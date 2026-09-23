"""The Port class — a user's entry point to their quilts.

A Port is:
- One user identity (user_id, token)
- One or many quilts (the destinations it can address)
- A projection (which surface tier)
- A witness chain (every operation is receipted)

Wraps the substrate walker for multi-tenancy.
"""
from __future__ import annotations

import asyncio
import datetime
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from ._vendor.mavis_substrate_walker import (
    Witness,
    WitnessChain,
    WitnessKind,
    hash_witness,
    fnv1a_64,
)


class Projection(str, Enum):
    """The four abstraction tiers a Port can speak.

    SPIRIT (Sept 23, 2026) — every projection emits the same witness chain;
    they differ in surface and emit format.
    """
    ESP32 = "esp32"      # embedded; C/Verilog codegen; CoAP or WebSocket; signed
    PYTHON = "python"    # application; SDK; type hints; pip-installable
    WEB = "web"          # server; REST + OpenAPI 3.1
    IDEATION = "ideation"  # chat; AI-Writings integration; async


@dataclass
class PortReceipt:
    """A receipted operation result.

    Receipts are first-class objects in the port. Every `.cell()`,
    `.record()`, `.witness()` returns a PortReceipt with at least:
    - content_hash (the witness's hash)
    - timestamp
    - tier (which projection issued this)
    - parent_hashes (chain anchors)
    """
    content_hash: str
    timestamp: str
    tier: Projection
    operation: str
    parent_hashes: List[str]
    payload: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_witness(cls, w: Witness, tier: Projection) -> "PortReceipt":
        return cls(
            content_hash=w.content_hash,
            timestamp=w.timestamp,
            tier=tier,
            operation=w.kind.value,
            parent_hashes=list(w.parent_hashes),
            payload=dict(w.payload),
        )


@dataclass
class Port:
    """A user's port to one or many quilts.

    Example:
        port = Port(
            user_id="casey",
            projection=Projection.PYTHON,
            quilts=["my-ledger", "my-cellforge-instance"],
        )
        async with port.session() as session:
            cell = await session.cell("weights/dense")
            receipt = await session.record({"step": 1, "weight": 0.42})
    """
    user_id: str
    projection: Projection = Projection.PYTHON
    quilts: List[str] = field(default_factory=list)
    token: Optional[str] = None
    endpoint: str = "https://port.workers.dev"
    # Per-port witness chain
    witness_chain: WitnessChain = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'witness_chain',
                          WitnessChain(substrate_id=f"port_{self.user_id}"))

    @property
    def port_id(self) -> str:
        return f"{self.user_id}:{self.projection.value}"

    def __repr__(self) -> str:
        return f"<Port user_id={self.user_id!r} projection={self.projection.value!r} quilts={self.quilts!r}>"

    @asynccontextmanager
    async def session(self):
        """Open a session against one or many quilts. Every operation witnessed.

        The session itself emits LOAD + SAVE witnesses, plus one witness per op.
        """
        # Bound instance variable needed by the session.
        sess = PortSession(self)
        try:
            yield sess
        finally:
            await sess.close()

    def witness_chain_verify(self) -> bool:
        """Re-derive every witness hash from residue."""
        return self.witness_chain.verify()

    def emit_witness_sync(self, kind: WitnessKind, payload: Dict[str, Any],
                          ) -> Witness:
        """Synchronous witness emit (for non-async code paths like the
        Ideation chat surface, which can be event-driven).

        Most users should use the async `session()` context.
        """
        w = Witness(
            kind=kind,
            substrate_id=f"port_{self.user_id}",
            payload=payload,
            parent_hashes=[],
        )
        self.witness_chain.append(w)
        return w


class PortSession:
    """An active session against a Port. Async by default."""

    def __init__(self, port: Port):
        self.port = port
        self._closed = False
        # Emit the LOAD witness
        self.port.witness_chain.append(Witness(
            kind=WitnessKind.LOAD,
            substrate_id=f"port_{self.port.user_id}",
            payload={
                "user_id": self.port.user_id,
                "projection": self.port.projection.value,
                "quilts": list(self.port.quilts),
            },
            parent_hashes=[],
        ))

    async def cell(self, cell_id: str) -> Any:
        """Read a cell from the addressed quilt."""
        if self._closed:
            raise RuntimeError("session closed")
        # Dispatch to projection-specific read
        from .projections import python as py_proj
        cell = await py_proj.read_cell(self.port, cell_id)
        self.port.witness_chain.append(Witness(
            kind=WitnessKind.WALK,
            substrate_id=f"port_{self.port.user_id}",
            payload={"op": "cell", "cell_id": cell_id, "preview": str(cell)[:80]},
            parent_hashes=[],
        ))
        return cell

    async def record(self, payload: Dict[str, Any], to_quilt: Optional[str] = None
                      ) -> PortReceipt:
        """Witness a custom observation into the chain."""
        if self._closed:
            raise RuntimeError("session closed")
        from .projections import python as py_proj
        await py_proj.write_cell(self.port, payload, quilt=to_quilt)
        witness = Witness(
            kind=WitnessKind.STITCH,
            substrate_id=f"port_{self.port.user_id}",
            payload={"op": "record", "to_quilt": to_quilt or "<auto>", **payload},
            parent_hashes=[],
        )
        self.port.witness_chain.append(witness)
        return PortReceipt.from_witness(witness, self.port.projection)

    async def promote(self) -> PortReceipt:
        """Graduate the chain's accumulated witnesses to a canonical finding.

        In v0.1, this is a stub that emits a PROMOTE witness. The canon
        promotion gate (JEV at p>0.7, or cost-plus "this tier transitions
        to that tier" rules) is upstream of the actual promotion.
        """
        if self._closed:
            raise RuntimeError("session closed")
        witness = Witness(
            kind=WitnessKind.PROMOTE,
            substrate_id=f"port_{self.port.user_id}",
            payload={
                "n_witnesses": self.port.witness_chain.size(),
                "n_finding_attempt": "v0.1-stub",
            },
            parent_hashes=[],
        )
        self.port.witness_chain.append(witness)
        return PortReceipt.from_witness(witness, self.port.projection)

    async def close(self):
        """Emit the SAVE witness; close the session."""
        if not self._closed:
            witness = Witness(
                kind=WitnessKind.SAVE,
                substrate_id=f"port_{self.port.user_id}",
                payload={
                    "n_witnesses": self.port.witness_chain.size(),
                    "duration_op": "<seconds>",
                },
                parent_hashes=[],
            )
            self.port.witness_chain.append(witness)
            self._closed = True


# ----- Convenience constructors -----


def make_port(user_id: str, projection: str = "python",
              quilts: Optional[List[str]] = None, **kwargs) -> Port:
    """Construct a Port from string args."""
    return Port(
        user_id=user_id,
        projection=Projection(projection),
        quilts=quilts or [],
        **kwargs,
    )
