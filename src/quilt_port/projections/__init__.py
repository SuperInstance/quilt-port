"""Projections — the four abstraction tiers a Port can speak.

Each projection has the same surface API:
- read_cell(port, cell_id) -> value
- write_cell(port, payload, quilt) -> None
- emit_format(port, receipt) -> serialized form

They differ in:
- Wire format (JSON, protobuf, signed-binary)
- Latency budget (50ms for ESP32, 5000ms for Ideation)
- Trust model (signed for ESP32, bearer for Web, etc.)

All four call back into the same Port witness chain.
"""
from . import python
from . import web
from . import esp32
from . import ideation
