"""Local runtime — for development and tests.

Stores port state in-memory. Mirrors the CF Worker runtime's interface.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from ..port import Port


# Per-port in-memory cell store. For tests only.
_CELLS: Dict[str, Dict[str, Any]] = {}


def _port_storage_key(port: Port) -> str:
    return f"{port.user_id}:{port.projection.value}"


async def read_cell(port: Port, cell_id: str) -> Any:
    cells = _CELLS.setdefault(_port_storage_key(port), {})
    return cells.get(cell_id)


async def write_cell(port: Port, payload: Dict[str, Any], quilt: Optional[str] = None
                      ) -> None:
    cells = _CELLS.setdefault(_port_storage_key(port), {})
    # Write under cell_id derived from payload, or a default key.
    key = payload.get("cell_id", "default")
    cells[key] = payload


async def reset_port(port: Port) -> None:
    """Reset a port's local state. Useful in tests."""
    _CELLS.pop(_port_storage_key(port), None)
