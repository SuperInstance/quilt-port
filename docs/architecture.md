# quilt-port architecture

**v0.1.0 — initial scaffold, 4 projections, 16 tests, fleet canary 49/49**

## The five layers

```
┌─────────────────────────────────────────────────────────────┐
│  USER                                                        │
│   • User identity (per port_id)                              │
│   • Authentication (bearer token / device cert / API key)    │
│   • One or many quilts                                       │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  PROJECTION LAYER                                            │
│   • ESP32  (C / Verilog codegen → Arduino sketch / FPGA net) │
│   • Python (type-hinted SDK, pip-installable)                │
│   • Web    (REST + OpenAPI 3.1)                              │
│   • Ideation (chat-driven, async, AI-Writings)              │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  PORT                                                        │
│   • Session (LOAD/WALK/STITCH/PROMOTE/SAVE witnesses)        │
│   • Witness chain (per-port, hash-chained, FNV1a-64)         │
│   • Quilt addressing (one port → many quilts)               │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  SUBSTRATE WALKER                                            │
│   • mavis-substrate-walker (vendored)                        │
│   • Discovers and walks any substrate                       │
│   • Same chain law as cellforge / moth-* / lexical-*         │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  SUBSTRATE (any of these)                                    │
│   • cellforge workbook                                      │
│   • moth-corpus surface                                       │
│   • moth-honest attack surface                               │
│   • moth-ledger trial balance                                │
│   • lexical-substrate variance ledger                        │
│   • morphic-canvas GPU                                       │
│   • (any substrate registered with the walker)               │
└─────────────────────────────────────────────────────────────┘
```

## The receipt flow

Every interaction follows the same 5-step protocol:

1. **LOAD** — opening a session emits a LOAD witness
2. **WALK** — reads emit WALK witnesses
3. **STITCH** — writes emit STITCH witnesses (the operator's signature)
4. **PROMOTE** — graduation to canon emits a PROMOTE witness
5. **SAVE** — closing emits a SAVE witness

This is the same as the substrate walker's protocol, lifted to the user-facing API. The user never sees the witnesses but they are all there, persistent, queryable.

## Cost model

The cost-plus model recovers raw CF billable cost + 30% margin:

```
raw_cost_usd    = sum(billable.unit_cost * quantity)
cost_plus_usd   = raw_cost_usd * (1 + MARGIN)
                                MARGIN = 0.30
```

For 100k requests per month, a typical port costs ~$0.50 raw (≈$0.65 cost-plus).

The pricing page should expose the same line items. **No rent extraction.**

## Domain strategy

| TLD  | Status | Use |
|------|--------|-----|
| `quilt.studio` | TBD | Creative / ideation-tier |
| `quilt.dev`    | TBD | Developer / Python-tier |
| `quilt.cloud`  | TBD | Cloud / hosted |
| `port-{user}.workers.dev` | **default** | Personal port URLs |

`.ai` is fading — see WORKSHOP.md §5 for the rationale. The brand is the tier, not the TLD.

## The four projections, in depth

### Python (PIP-installable, type-hinted)

```python
from quilt_port import Port

port = Port(user_id="casey", projection="python", quilts=["q1"])
async with port.session() as s:
    cell = await s.cell("w/dense")
    receipt = await s.record({"step": 1, "weight": 0.42})
```

### Web (REST + OpenAPI)

```
GET  /v1/cells/{cell_id}                  # read a cell
POST /v1/cells/{cell_id}                  # write a cell
GET  /v1/quilts/{q}/witnesses             # paginated witness listing
POST /v1/quilts/{q}/promote               # graduate a chain
```

OpenAPI spec available at `quilt_port.projections.web.openapi_spec()`.

### ESP32 (codegen target)

Generates Arduino sketches and Verilog modules. The user includes the generated library in their firmware. Each read/write is signed on the device; receipts travel back.

### Ideation (chat-driven)

Each chat turn is a witness. The user's canon accrues from each conversation. AI-Writings front-end integrates async.

## Hosting model

| tier | audience | revenue model |
|------|----------|---------------|
| Free + ads | Casual web | Light ad injection (or sponsorship) |
| Cost-plus | Developers, makers | Raw CF cost + 30% margin |
| Premium | Enterprises | SLA, dedicated capacity |

Open-source everything; hosted layer adds SLA, billing, durability.

## Deployment

```bash
# OSS self-host (anyone can do this):
wrangler deploy

# Hosted (us):
# - Each port = 1 Durable Object
# - D1 stores port metadata
# - KV stores rate-limit counters
# - R2 stores witness chain archive
# - Pages serves the management UI
```

## Substrate compatibility

The port surface is substrate-agnostic. A port's quilt can be any substrate that's registered with the walker:

```
cellforge       → Workbook.witness_log  (per-cell witnesses)
moth-corpus     → SURFACE/v1 corpus.jsonl  (per-row hashes)
lexical         → variance ledger  (per-entry variance)
moth-honest     → planted ground truth  (per-evaluation witness)
morphic-canvas  → GPU buffer (TBD)
```

The same Python projection works across all five substrates.

## What ships in v0.1.0

- `Port` class with `session()`, `cell()`, `record()`, `promote()`, `close()`
- Python projection (working, local runtime)
- Web projection (REST + OpenAPI shape, sketch implementation)
- ESP32 projection (Arduino + Verilog codegen)
- Ideation projection (chat-driven, v0.1 stub)
- Cost-plus billing model with `Billable`, `Meter`, `quote_request_breakdown()`
- Local runtime (in-process, for dev/tests)
- Cloudflare Worker runtime (sketch, full impl in Phase 2)
- 16 tests, all passing
- Vendored `mavis-substrate-walker` so the repo ships standalone
- Fleet canary verified — 49/49 polyformal

## What's deferred

- Real Cloudflare Worker runtime (Phase 2)
- Real CF DO backing per port (Phase 2)
- Real ad injection (free tier currently has no ads)
- Real WS-AI inference in ideation tier (Phase 4)
- Real ESP32 firmware signing + transport (Phase 5)
- Premium tier features (Phase 6)

## Future hooks

- Ad-sponsored ports (with brand-acceptable ad injection)
- Custom domain support (pay tier)
- Multi-user ports (organizations, teams)
- Port-to-port cross-witnessing (a port can address another port as a quilt)
- Bridge to AI-Writings as a publication surface (each port has an AI-Writings page)
