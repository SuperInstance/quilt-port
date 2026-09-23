# quilt-port

**The user's port to their quilts.** Open-source SDK + cost-plus hosted service. One user identity; four projections (ESP32 / Python-TS / Web-REST / Ideation-AI-Writings); receipts at every step.

## What is a port?

A `Port` is your single user identity with the Quilt. It authenticates you, holds your witness chain, and addresses your quilts. The same Port can be reached from any of four projections:

| Projection | Audience | Surface |
|------------|----------|---------|
| **ESP32** | Embedded developers, sensor-network builders | C / Verilog / Arduino code-gen targets; CoAP or WebSocket |
| **Python** | App developers, ML teams | `pip install quilt-port` — type-hinted SDK |
| **Web** | Server integrators | REST / OpenAPI 3.1 spec |
| **Ideation** | AI-Writings readers, "diamond-miners" | Chat interface, async, multi-turn |

All four project from one substrate walker. Same canon, same witness chain, four access surfaces.

## Why this exists

We're building the user-facing gateway to the Quilt fleet:

- `cellforge` — AI training substrate (cells, witness chain, dispatcher)
- `moth-corpus`, `moth-cells`, `moth-honest`, `moth-ledger` — the receipted hunting family
- `morphic-canvas` — GPU substrate
- `lexical-substrate` — bitwise-algebra sibling
- `mavis-substrate-walker` — the cross-substrate protocol
- `mavis-fleet` — the orchestration spine

Each substrate is a quilt. The Port addresses one or many of your quilts and emits a witness for every step.

## Quick start (Python projection)

```python
from quilt_port import Port

port = Port(
    user_id="casey",
    projection="python",
    quilts=["my-ledger", "my-cellforge-instance"],
)

async with port.session() as session:
    cell = await session.cell("weights/dense")
    receipt = await session.record({"step": 1, "weight": 0.42})
    print(receipt.content_hash)
```

## Quick start (Ideation tier / AI-Writings chat)

```python
from quilt_port import IdeationPort

chat = IdeationPort(projection="ideation", user_id="casey")
async for turn in chat.stream("give me the receipt for last night's run"):
    print(turn.text, turn.attached_witness)
```

## Quick start (ESP32)

```cpp
#include "quilt_port_esp32.h"

QuiltPortClient port("quilt-port-casey-esp32", "https://port.example.com");
auto cell = port.get_cell("sensor/temperature");
port.record(sensor_reading);  // signed receipt
```

## Open-source + cost-plus

Following the LangChain / n8n / CrewAI pattern:

- **Open-source**: the Port class, all four projections, the witness chain, the substrate walker.
- **Hosted (cost-plus)**: Cloudflare Workers backend. Pricing is **what it costs us + ~30% margin** — no rent extraction. Anyone can fork the OSS, deploy to their own CF account, and run it themselves.

## Domain strategy

`.ai` as a TLD is fading — soon users will pick the ecosystem, not the label. We default to:

- `port-{user}.workers.dev`
- `quilt.studio`, `quilt.dev`, `port.studio`, etc.
- Custom domains (pay tier allows CNAME)

## Workshop & iteration

This repo's `WORKSHOP.md` is the live workshop doc — open questions, multi-angle debate, the four-tier typology, the cost-plus rationale. Each round of conversation updates it.

## Versions

- v0.1.0 — initial scaffold: Port class, Python projection (works), Web/ESP32/Ideation projections (sketches), `cost-plus` billing stub, fleet canary `0x24a555471370b18d` preserved, 10 tests.

## Doctrine (the substrate-walker connection)

`quilt-port` is the user-facing gateway. The actual cross-substrate protocol is `mavis-substrate-walker`. The Port is the same walker with multi-tenancy and tier-specific projections.

**Three primitives survive every layer** (from `inter-logistical-reasoning`):

- **STITCH** — connect a user's tier to the walker
- **WITNESS** — receipt every step
- **PROMOTE** — graduate receipts to canon-worthy findings

A user using `quilt-port` does all three without knowing the words. The highest abstractions still reduce to the smallest primitives.

## Files

- `WORKSHOP.md` — the workshop doc, 16 sections, iterate here
- `src/quilt_port/port.py` — the `Port` class
- `src/quilt_port/projections/python.py` — Python projection (works)
- `src/quilt_port/projections/web.py` — Web projection (sketch)
- `src/quilt_port/projections/esp32.py` — ESP32 projection (sketch)
- `src/quilt_port/projections/ideation.py` — Ideation projection (sketch)
- `src/quilt_port/billing/cost_plus.py` — Cost-plus billing model
- `src/quilt_port/runtime/cloudflare.py` — Cloudflare Worker runtime
- `docs/architecture.md` — diagrams + tier details

## License

MIT.
