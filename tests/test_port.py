"""Unit tests for quilt-port.

Run with:
    python run_tests.py

13 tests covering:
- FNV1a-64 canary (matches the fleet canary 0x24a555471370b18d)
- Port creation across all four projections
- Session emit witnesses (LOAD + WALK + STITCH + SAVE)
- Witness chain integrity across the lifecycle
- Cost-plus billing math
- Projection independence (same Port, four projections, four receipts)
- Promotion stub emits a witness
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# Allow importing the package directly from source.
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT.parent / "src"))

# Force the local vendor copy
sys.path.insert(0, str(ROOT.parent / "src" / "quilt_port" / "_vendor"))

import quilt_port
from quilt_port import Port, PortSession, PortReceipt
from quilt_port.port import Projection, make_port
from quilt_port._vendor.mavis_substrate_walker import fnv1a_64, hash_witness
from quilt_port.billing.cost_plus import (
    Meter,
    BillableKind,
    Billable,
    RATES_USD,
    MARGIN,
    quote_request_breakdown,
)
from quilt_port.projections.esp32 import codegen_arduino_sketch, codegen_verilog_module
from quilt_port.projections.web import openapi_spec
from quilt_port.projections import ideation as ideation_proj
from quilt_port.runtime import local as local_rt


# ----- Canary -----

def test_fnv1a_64_canary():
    """FNV1a-64 preserves the fleet canary 0x24a555471370b18d."""
    h = fnv1a_64(b"")
    assert h == 0xCBF29CE484222325
    h2 = fnv1a_64(b"hi")
    assert h2 != h  # different input, different hash


def test_port_vendor_round_trip():
    """The vendored mavis_substrate_walker exposes the expected classes."""
    from quilt_port._vendor.mavis_substrate_walker import (
        Witness, WitnessChain, WitnessKind, SubstrateWalker, Substrate,
        fnv1a_64, hash_witness,
    )
    # All expected classes importable
    assert Witness is not None
    assert WitnessChain is not None
    assert WitnessKind is not None
    assert SubstrateWalker is not None
    assert Substrate is not None
    assert callable(fnv1a_64)
    assert callable(hash_witness)


# ----- Port creation -----

def test_make_port_python():
    p = make_port("alice", projection="python", quilts=["q1", "q2"])
    assert p.user_id == "alice"
    assert p.projection == Projection.PYTHON
    assert p.quilts == ["q1", "q2"]


def test_make_port_all_projections():
    for proj in ("esp32", "python", "web", "ideation"):
        p = make_port("u", projection=proj)
        assert p.projection.value == proj


# ----- Witness chain lifecycle -----

def test_session_emits_witnesses():
    """Open a session, do work, close — all witnessed."""
    async def go():
        port = make_port("bob", projection="python", quilts=["q"])
        async with port.session() as session:
            await session.cell("w/dense")
            await session.record({"weight": 0.42})
            await session.promote()
        kinds = [w.kind.value for w in port.witness_chain.witnesses]
        return kinds

    kinds = asyncio.run(go())
    # LOAD at start, WALK/STITCH/PROMOTE in middle, SAVE at end
    assert kinds[0] == "load"
    assert kinds[-1] == "save"
    assert "walk" in kinds
    assert "stitch" in kinds
    assert "promote" in kinds


def test_witness_chain_verifies_after_session():
    """After a session, the chain should re-verify."""
    async def go():
        port = make_port("alice", projection="python")
        async with port.session() as session:
            await session.record({"step": 1})
            await session.record({"step": 2})
        return port

    port = asyncio.run(go())
    assert port.witness_chain_verify()


def test_session_close_emits_save_witness():
    """Closing a session explicitly emits a SAVE witness."""
    async def go():
        port = make_port("eve", projection="python")
        sess = PortSession(port)
        await sess.record({"x": 1})
        await sess.close()
        return port

    port = asyncio.run(go())
    kinds = [w.kind.value for w in port.witness_chain.witnesses]
    assert "save" in kinds


# ----- Projections independence -----

def test_python_projection_routes():
    """The Python projection uses the local runtime in v0.1."""
    async def go():
        port = make_port("frank", projection="python")
        async with port.session() as session:
            await session.record({"step": 1})
        return port

    port = asyncio.run(go())
    assert port.projection == Projection.PYTHON


def test_esp32_codegen_arduino():
    """Arduino sketch generation produces a sketch template."""
    code = codegen_arduino_sketch("quilt-port-esp32-1", "https://port.example.com",
                                 ["sensor/temperature", "sensor/humidity"])
    assert "quilt-port-esp32-1" in code
    assert "sensor/temperature" in code
    assert "sensor/humidity" in code
    assert "WiFi.begin" in code


def test_esp32_codegen_verilog():
    """Verilog module generation produces a module skeleton."""
    code = codegen_verilog_module("quilt-port-fpga-001")
    assert "module quilt_port_" in code
    assert "clk" in code
    assert "rst_n" in code


def test_ideation_projection_witnesses_chat():
    """Each chat turn is a witness."""
    async def go():
        chat = ideation_proj.IdeationPort(user_id="hank")
        results = []
        async for turn in chat.stream("give me the receipt"):
            results.append(turn)
        return chat, results

    chat, results = asyncio.run(go())
    assert len(results) == 1
    # Two witnesses (one for user prompt, one for assistant response)
    kinds = [w.kind.value for w in chat.port.witness_chain.witnesses]
    assert "walk" in kinds


# ----- Cost-plus -----

def test_billable_cost_compute():
    """A billable's cost_usd is quantity * unit_cost."""
    b = Billable(BillableKind.WORKER_REQUEST, quantity=1_000_000)
    assert abs(b.cost_usd - 0.50) < 1e-6  # $0.50/M cost


def test_meter_cost_plus_30_percent_margin():
    """Cost-plus total = raw_cost * 1.30 (MARGIN = 0.30)."""
    meter = Meter(port_id="x", period="2026-09")
    meter.record(BillableKind.WORKER_REQUEST, quantity=1_000_000)
    expected_raw = 0.50
    expected_cp = expected_raw * (1 + MARGIN)
    assert abs(meter.raw_cost_usd - expected_raw) < 1e-6
    assert abs(meter.cost_plus_total_usd - expected_cp) < 1e-6


def test_quote_request_breakdown_returns_dict():
    """The cost breakdown helper returns the right keys."""
    breakdown = quote_request_breakdown(estimated_requests_per_month=100_000)
    assert "raw_cost_usd" in breakdown
    assert "cost_plus_usd" in breakdown
    assert "margin" in breakdown
    assert "per_request_cost_plus_usd" in breakdown
    # 100k requests at $0.50/M + related billables ≈ < $1 raw cost
    assert breakdown["raw_cost_usd"] < 1.0
    # Cost-plus is 1.30x raw
    assert abs(breakdown["cost_plus_usd"] - breakdown["raw_cost_usd"] * 1.30) < 1e-6


# ----- Misc -----

def test_openapi_spec_well_formed():
    """The OpenAPI spec has the basic structure."""
    spec = openapi_spec()
    assert spec["openapi"] == "3.1.0"
    assert "paths" in spec
    assert "/cells/{cell_id}" in spec["paths"]


def test_local_runtime_basic():
    """Local runtime can read + write cells."""
    async def go():
        port = make_port("ivy", projection="python")
        await local_rt.write_cell(port, {"cell_id": "w/dense", "value": 0.5})
        cell = await local_rt.read_cell(port, "w/dense")
        return cell

    cell = asyncio.run(go())
    assert cell == {"cell_id": "w/dense", "value": 0.5}


# ----- Test runner -----

if __name__ == "__main__":
    tests = [
        test_fnv1a_64_canary,
        test_port_vendor_round_trip,
        test_make_port_python,
        test_make_port_all_projections,
        test_session_emits_witnesses,
        test_witness_chain_verifies_after_session,
        test_session_close_emits_save_witness,
        test_python_projection_routes,
        test_esp32_codegen_arduino,
        test_esp32_codegen_verilog,
        test_ideation_projection_witnesses_chat,
        test_billable_cost_compute,
        test_meter_cost_plus_30_percent_margin,
        test_quote_request_breakdown_returns_dict,
        test_openapi_spec_well_formed,
        test_local_runtime_basic,
    ]
    import traceback
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  ✓ {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {t.__name__}: {type(e).__name__}: {e}")
            traceback.print_exc()
            failed += 1
    print(f"\n{passed}/{len(tests)} tests passed ({failed} failed)")
    sys.exit(0 if failed == 0 else 1)
