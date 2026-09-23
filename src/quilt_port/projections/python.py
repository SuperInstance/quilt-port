"""Python projection — the v0 fastest to ship.

Surface:
- async read_cell(port, cell_id) -> value (dict)
- async write_cell(port, payload, quilt) -> None

Wire format: JSON over HTTP (via CF Worker runtime).
Trust: bearer token (sign up → token issued)
Latency budget: 200ms
"""
from __future__ import annotations

import asyncio
from typing import Any, Dict, Optional

from ..port import Port, PortSession
from ..runtime import local as local_rt


async def read_cell(port: Port, cell_id: str) -> Any:
    """Read a cell from the addressed quilt over the Python projection.

    In v0.1, this is a local call — no HTTP — using an in-memory
    substrate. The CF Worker runtime takes over for hosted mode.
    """
    rt = _runtime_for(port)
    return await rt.read_cell(port, cell_id)


async def write_cell(port: Port, payload: Dict[str, Any], quilt: Optional[str] = None
                      ) -> None:
    """Write a cell. Witnessed on the port's chain (caller adds the witness)."""
    rt = _runtime_for(port)
    await rt.write_cell(port, payload, quilt=quilt)


def _runtime_for(port: Port):
    """Pick the runtime: local for development, cloudflare for hosted."""
    # In v0.1: always local. CF path will be added in Phase 2.
    from ..runtime import local
    return local
