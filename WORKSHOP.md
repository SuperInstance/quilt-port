# Workshop — `quilt-port`: the user's port to their quilts

**Date**: Sept 23, 2026
**Author**: Mavis + Casey
**Trigger**: *Casey's prompt about a production API for users, open-source + cost-plus, on Cloudflare Workers, with multiple abstraction tiers (ESP32 / Python / Verilog / AI-Writings ideation).*
**Status**: **DRAFT** — this doc is meant to be iterated, not finalized. Each round of conversation will sharpen it.

---

## TL;DR

**`quilt-port`** is a production API and open-source codebase that gives every user **a personal port to their quilts**. A port is one user identity with multiple projections:

- **ESP32-tier** — embedded boards talking to the port over a thin C/Verilog-friendly interface
- **Python/TS-tier** — application developers using the SDK
- **Web-tier** — REST/OpenAPI for app-server integrations
- **Ideation-tier** — chat-driven diamond-mining through AI-Writings

All four projections are **the same substrate walker** serving different abstraction layers. The economics follow the LangChain/n8n/CrewAI pattern: **open-source the canon, host the convenience** — *cost-plus*, not extractive, with multiple revenue models (free-ad-supported for casual web, cost-plus for developers, premium for enterprises).

`.ai` as a TLD is fading — users will pick the ecosystem, not the label. Domain strategy therefore covers broader TLDs (.studio, .quilt if we can get it, generic .workers.dev subdomains).

---

## 1. The conceptual frame in Casey's own words

> *"we open source everything but we have a nice cost-plus hosted version... free to the user and either is paid for by minimal ads if its a webservice like handling porting around the internet for various inter-quilt work, or backend cloudflare workers acting as everything from chat bots to image gen to embedding and storing d1 and other data for our users"*
> *"ai as an idea will fade because what type will become the question... using a word processor later became which one matter... it depend on what eco system you are use to"*
> *"esp32 needs a low-level language compared to a highly dynamic large network quilt wanting python and typescript... some who want raw verilog because they are thinking truly ground up... and still others who want to ideate themselves on the actual hard-functions and dance through ai-writings like a miner looking for diamonds"*

**The core idea**: every user gets a port. A port is a single user identity, with their authentication, their witness chain, their quilt(s), and a projection layer chosen by their context.

**Why this matters**: the substrate walker doctrine (Sept 23, 2026 — `mavis-substrate-walker` v0.1.0) says we already have **the mechanism** for cross-substrate work. What's missing is **the product surface**. `quilt-port` is that surface.

---

## 2. What is a port?

A port in this sense has two metaphors:

- **Network port** (e.g., TCP port 443): a numbered channel. Each user's port has an endpoint — `port-{user_id}.quilt.workers.dev` or `port-{handle}.example.com`.
- **Ship's port**: a hub where things come in and go out. The user's "home base" for their quilts.

A port has:
- **An endpoint** (URL/API surface)
- **An identity** (who's calling — token + tier)
- **A projection** (which abstraction tier is the user on)
- **A witness handle** (their state history)
- **Cost-plus billing** (how their usage translates to cost)
- **One or many quilts** (the destinations the port can address)

The port is NOT a model. The port doesn't carry data. **The port is the substrate walker running with the user's identity, in the user's abstraction tier.** Following the doctrine from `inter-logistical-reasoning`: the port is *performative, not representational*.

---

## 3. The four abstraction tiers (Casey's user types)

| Tier | Audience | Interface | Latency target | Tech |
|------|----------|-----------|----------------|------|
| **ESP32-tier** | Embedded developers, sensor-network builders | C / Verilog / Arduino code-gen targets; protobuf over CoAP or websocket | < 50 ms | Tiny code generation, signing, low-RAM targets |
| **Python-tier** | Application developers, prototyping, ML/DL teams | Python SDK with full type hints; SDK autodownloads the port cert | < 200 ms | `pip install quilt-port` |
| **Web-tier** | Server integrators, app-server teams | REST / OpenAPI 3.1 spec; first-class serverless targets | < 500 ms | CF Workers, Nitro, etc. |
| **Ideation-tier** | Non-developers, AI-Writings readers, "diamond-miners" | Chat interface, voice, AI-Writings integration; async; multi-turn | async, slow-OK | LLM-mediated |

All four project from **one substrate walker**. Same canon, same witness chain, different access surface.

### Why four and not one

Each tier's users have radically different defaults:

- **An ESP32 farmer** has intermittent connectivity, kilobytes of RAM, no display. They need signed receipts, not conversations.
- **A Python app-dev** wants `async with quilt_port.open() as port:` and type hints everywhere.
- **A web developer** wants CI/CD-friendly OpenAPI specs.
- **A diamond-miner** wants to think out loud in AI-Writings and have the canon accrue from their explorations.

Forcing one interface onto all four means optimizing for the lowest common denominator (typically the embedded tier — slow, text-only). Better: **emit the same canon, project it to the right shape.**

---

## 4. The cost-plus economics

The pattern is identical to LangChain, n8n, CrewAI:

| tier | audience | revenue model | UX |
|------|----------|---------------|-----|
| **Free + ads** | Casual web users | Light ad injection in the chat/render (most ad-free paths still exist) | Free with ad slots |
| **Cost-plus** | Developers, makers, students | Charge what it costs us + ~30% margin; transparent | Pay-as-you-go |
| **Premium** | Enterprises | SLA, dedicated capacity, audit trail | Contract-backed |

The key word is **cost-plus**: not extractive, not rent-seeking. **We charge what it costs us to run it, plus a fair margin.** That leaves the user with prices that are obviously fair, the developer with prices they can predict, and us with a stable business.

### What "what it costs" means

- Cloudflare Workers billable requests ($0.50/M requests on Workers Paid)
- D1 row reads/writes ($0.001/M, $1/M)
- Workers AI inferences ($0.011/M input tokens for some models)
- KV reads/writes ($0.50/M)
- Storage (R2, $0.015/GB-month)

The cost-plus API: a request costs us ~$0.0000015 in CF billables. We charge ~$0.000005. The user sees a transparent pricing page with line items that match our billables + margin.

### Why no-extractive matters

If users fork the OSS, deploy their own CF Worker, and self-host — we want that to **just work, at lower performance and no SLA**. That's the OSS path. We never compete by lock-in; we compete by **hosting convenience that's good enough that even the forkable users pay for it**.

This is the open-core pattern done honestly. The OSS is canon-complete. The hosted is "I don't want to run this myself."

---

## 5. Domain strategy — the two-layer answer

Casey named the top candidates. Two layers, two domains, two stories.

### Layer 1 — `superinstance.dev` (the general-purpose gateway)

> "superinstance.dev this is very general-purpose and by routing everything through it, the name superinstance has an implied meaning that a zero-shot human or agent would probably infer a quilt-like system. they might not guess spreadsheet abstraction, they might think flow-chart or hub-and-spokes wheel. but the direction of thought is in the name."

The umbrella. The first URL a zero-shot visitor hits. The name encodes:

- **super-instance** — many things, one entry
- **quilt-like** — connected, layered, not a single thing
- **General-purpose** — anyone can come here for any quilt tool

URL patterns:
- `superinstance.dev` — landing
- `docs.superinstance.dev` — documentation
- `app.superinstance.dev` — the management UI
- `port-{user}.superinstance.dev` — per-user port

### Layer 2 — `purplepincher.org` (the agent identity layer)

> "purplepincher.org is another candidate we already own. the pincher part is going to lead someone to think agent with openclaw ubiquitous. and as a popular aquarium pet, many will intuitively get the hermit-crab analogy we often use for the relationship between a harness and it's model."

The crab's address. The agent identity layer. The name encodes (in increasing depth):

1. **Pincher** → agent with openclaw, ubiquitous
2. **Purple pincher** → *Coenobita clypeatus*, the most popular aquarium hermit crab — intuitively familiar
3. **The hermit-crab analogy** → the model is the shell, the code is the rigging, the data is alive
4. **The counterintuitive ah-ha** → "linear algebra is soft around the rigid frame of a classical algebraic harness"; "the model is the one thing I'd have to find a new one of to go fishing"

The deeper meaning only clicks when users read the [Hull Doctrine](./HULL_DOCTRINE.md) (canon, see `HULL_DOCTRINE.md`). When they do, they get a double-edged sword moment: the naming is *both* playful *and* load-bearing.

URL patterns:
- `purplepincher.org` — landing for the agent-as-crab identity
- `{user}.purplepincher.org` — per-user crab identity
- `port-{user}.purplepincher.org` — per-user port as their crab's door
- `doctrine.purplepincher.org` — the Hull Doctrine page

### Why both, not one

The two-domain strategy is **layered, not redundant**:

| | `superinstance.dev` | `purplepincher.org` |
|---|---|---|
| **First impression** | "Quilt-like system, many things" | "Agent with claws, hermit crab" |
| **Audience** | Anyone new | Agent-first users, AI-literate |
| **Default for** | Documentation, OSS, dev-tier | Ideation-tier, personal crab |
| **Doctrine** | Tells the system model | Tells the agent ontology |
| **Backed by** | The Port class | The Hull Doctrine |

A user can have *both* — a port on `superinstance.dev` for general dev work, *and* a port on `purplepincher.org` for their personal-agent identity. The two ports share the same witness chain because the witness chain is the crab's equipment, not the URL's.

### `.ai` fading — confirmed

> "ai as an idea will fade because what type will become the question... using a word processor later became which one matter... it depend on what eco system you are use to"

Neither `superinstance.dev` nor `purplepincher.org` is `.ai`. Both names survive the fade because they don't carry the AI label. They carry *the type* and *the metaphor*.

### Domain portfolio (Cloudflare)

Casey said many domains are already registered. Inventory question: which ones? The two confirmed:

- `superinstance.dev` (already deployed for the docs site)
- `purplepincher.org` (already owned)

Other suggestions (cheaper than .ai):
- `quilt.{studio,cloud,dev,app}` — for specific sub-products
- `port.{studio,cloud,dev,app}` — for the port ecosystem
- `cellular.{studio,cloud,dev,app}` — for the cellular-architecture projects
- `substrate.{studio,cloud,dev,app}` — for the substrate walker family
- `mavis.{studio,cloud,dev,app}` — for the walker-as-named-personality
- `hull.{studio,cloud,dev,app}` — for the Hull Doctrine material (if it warrants a home)

---

## 6. Cloudflare Workers — the runtime

Casey named the stack: CF Workers + chat bots + image gen + embedding + D1 + storage. This is the right runtime:

| Layer | Service | Used for |
|-------|---------|----------|
| Compute | Cloudflare Workers | API handling, projection layer |
| Per-port state | Durable Objects | Each port = 1 DO with isolated witness chain |
| KV cache | Workers KV | Rate-limit counters, low-latency lookups |
| SQL | D1 | Quilt metadata, account info |
| Blob | R2 | Training data, archive of witness chains |
| AI inference | Workers AI | Embeddings, chat for ideation-tier |
| Pages | Pages | Static UI for hosted-port management |
| Schedule | Cron Triggers | Periodic witness compaction, billing roll-up |

Per-port Durable Object is the load-bearing primitive. Each user's port gets:
- A unique DO instance
- The substrate walker running inside it
- A witness chain scoped to that port
- Limited burst concurrency (Cost is bounded per port)

This is the exact architecture for hosted port infrastructure.

---

## 7. Positioning vs the market

| Competitor | What they do | Where Quilt-port differs |
|------------|--------------|--------------------------|
| **LangChain** | Python LLM orchestration | LangChain is Python-only, opinionated chains; Quilt-port is substrate-agnostic, tiered |
| **n8n** | Visual workflow automation | n8n is visual; Quilt-port is **witness-led**, no UI required, runs in any tier |
| **CrewAI** | Multi-agent collaboration | Quilt-port's `Witness` is the agent consensus — already receipted, not polyfilled |
| **Replicate** | Model hosting, cost-recovery | Replicate hosts *models*; Quilt-port hosts *the walker*. Different surface, same cost-plus |
| **Modal** | Serverless compute | Modal is a compute layer; Quilt-port is an *abstraction tier* |
| **OpenAI / Anthropic** | First-party inference | Quilt-port is the *receipt layer* above them; we don't compete on raw inference |

The unique selling point that none of these have:

> **Receipted-everything**. Every operation emits a witness. Every cross-tier handoff is receipted. Every billing event is receipted. Try auditing LangChain's billing — you can't. Try reproducing an n8n workflow exactly — you can't. Quilt-port's witness chain makes both trivial.

The honesty of cost-plus pricing is the second differentiator. We don't extract rent; we recover cost.

---

## 8. Open-source vs hosted — what goes where

Open-source (canonical, forkable):

- The substrate walker (`mavis-substrate-walker` v0.1.0)
- The `Port` class and its four projections (Python, ESP32, Web, Ideation)
- The witness chain implementation
- The cell model (cellforge + sister repos)
- The byte-level canonical representation (moth-ledger FNV1a-64 chain law)
- The CLI tooling

Hosted-only (the convenience-and-SLA layer):

- The cost-plus billing infrastructure
- The SLA-backed enterprise tier
- The ad injection layer for the free tier (when ads exist; current model doesn't need them — they may come later)
- The Cloudflare Workers deployment that ties it all together

This means **forking gives you everything the canon requires; running it in production gives you the convenience we built and the SLA we maintain.** The OSS community can verify the canon; the hosted customers get a working service.

---

## 9. The user-types — four perspectives on the same Port

Casey named them. Let's characterize each in three words:

1. **ESP32 user**: *constrain the canvas.* 
   - Talks to a webhookable endpoint with small payloads
   - Wants signed receipts (firmware update proof)
   - Doesn't have a screen. The receipt is the screen.

2. **Python/TS user**: *rapidly port the network.* 
   - `from quilt_port import Port; port = Port('handshake'); ...`
   - Wants type-hinted SDK + the kind of autocomplete LLMs give for pandas
   - Iterates fast; deploys often.

3. **Verilog user**: *think ground up.* 
   - Wants hardware descriptions of cells, witness nets, dispatcher state machines
   - Generates Verilog from the port's projection
   - Synthesizes for FPGA / ASIC. The witness chain becomes the trace buffer.

4. **AI-Writings / ideation user**: *diamond-mine.* 
   - Talks to the port in conversation
   - Each chat becomes a witness; the user navigates their canon through dialogue
   - The port learns what they are looking for.

All four project from the same walker. Differ in surface, framing, latency budget, and emit format.

---

## 10. What this looks like in code (sketch)

```python
# User-side Python
from quilt_port import Port

port = Port(
    user_id="casey",
    projection="python",  # tier
    quilts=["my-ledger", "my-cellforge-instance"],
)

# All operations are witnessed
async with port.session() as session:
    cell = await session.cell("weights/dense")  # read a cell
    receipt = await session.record({"step": 1, "weight": 0.42})
    print(receipt.content_hash)  # receipted at every step

# Or, the same Port at the IDEATION tier:
from quilt_port import IdeationPort
chat = IdeationPort(projection="ideation", user_id="casey")
async for turn in chat.stream("give me the receipt for last night's run"):
    print(turn.text, turn.attached_witness)

# And the ESP32 tier:
# /src/esp32/main.cpp (sketch)
#   #include "quilt_port_esp32.h"
#   QuiltPortClient port("quilt-port-casey-esp32", endpoint="https://port.example.com");
#   auto cell = port.get_cell("sensor/temperature");
#   port.record(sensor_reading);  // witnessed via signed receipt
```

Same Port. Three interface surfaces.

---

## 11. Open questions (workshop!)

These are the questions where Casey's input matters most:

1. **What does "free + ads" actually look like?** Casey mentioned ads as a revenue model — but ads and AI have a complex relationship. Better: free without ads, paid for premium features; or specific brand sponsorships for free tier ("Quilt: Powered by Stripe"); or promoted ports.

2. **Where does Mavis fit?** Mavis is the substrate walker. `quilt-port` IS Mavis-as-a-service with multi-tenancy. Is this the next org (like quilt-live-canon), or a new identity?

3. **Where to draw the line on proprietary?** Cost-plus billing is the core revenue. But is CF Worker deployment code OSS too? (Probably yes — anyone should be able to deploy their own instance.)

4. **Pre-existing domains**: Casey said many are registered. Need a list. Specific suggestion: `quilt.studio`, `port.studio`, `quilt.dev`, etc.

5. **How does pricing scale with usage?** Tokens? Cells touched? Witness chain length? All three are reasonable; need to pick the model that matches user mental model.

6. **How does the ESP32 tier authenticate?** Mutual TLS with device certs is the right call, but it's heavy for some users. Symmetric key with rate-limit + nonce? Bearer token + IP allow-list?

7. **Should the four tiers be four separate products or one product with four surfaces?** My instinct: one product. The Port has a `projection` field. The same instance can be accessed from any tier simultaneously.

8. **What's the relationship to cellforge / moth-* / lexical-*?** They're the substrates the port can address. A port connects to one or many substrates; the port emits a receipt when it does.

9. **What happens to a port when its user deletes their account?** Witness chain archival. Default: keep the chain (it's sacred — "no deletion" doctrine); user can mark `port_state=retired` but witness stays. R2 holds archives indefinitely.

10. **Where do we host?** First-party: Cloudflare. **Should we offer deployment to other CF Workers users' accounts?** Yes — that's the OSS self-hosted path.

---

## 12. What this simplifies the higher structures into words

**The three words, again: STITCH WITNESS PROMOTE.**

- The port `STITCH`es each tier's surface to the substrate walker
- The port `WITNESS`es every operation (kernel of the product)
- The port `PROMOTE`s receipts to canon-worthy findings (JEV gate at p>0.7, or cost-plus "this tier transitions to that tier" gates)

That three-word answer holds at every level. The port isn't a new invention — it's a projection of the existing walker doctrine onto multi-tenancy and cost economics.

A user using `quilt-port` is doing STITCH + WITNESS + PROMOTE without knowing the words. That's the goal: **the highest abstractions still reduce to the smallest primitives.**

---

## 13. The roadmap (6 phases)

### Phase 0 — Workshop (this doc)

Iterate on the angles. Get Casey to commit on:
- TLD direction
- Ad-supported tier's design
- Which of the four tiers is v0 (probably Python, since the SDK is fastest)
- Pre-existing domain inventory

### Phase 1 — Python-tier v0 (smallest shippable)

- `quilt-port` Python SDK
- Connection to the canonical substrate walker (`mavis-substrate-walker`)
- One Port, one quilt, one projection (Python)
- `cost-plus` billing in stub (no payments yet; just metering)
- 10-15 tests
- A demo notebook

### Phase 2 — Cloudflare Worker runtime

- CF Worker entry point
- Durable Object backing each port
- D1 schema for port metadata
- KV for rate-limit counters
- Deployable to user's CF account (OSS)

### Phase 3 — Web-tier v0 (REST + OpenAPI)

- OpenAPI 3.1 spec generated from the SDK
- REST endpoints that mirror the Python SDK
- Auth via bearer token (issue at signup)
- Static UI for managing ports (CF Pages)

### Phase 4 — Ideation-tier v0 (AI-Writings chat)

- Chat interface
- Each chat turn is a witness
- AI-Writings front-end integration (minimal API surface)
- Async, no latency SLA

### Phase 5 — ESP32-tier v0 (C/Verilog codegen)

- Codegen target that emits Arduino-sketch-style code
- Protobuf over WebSocket or CoAP
- Signed receipts (the user's firmware can verify them)

### Phase 6 — Premium tier (SLA + dedicated)

- Contract-backed
- Custom capacity
- Audit trail (CF Logpush into customer's R2 bucket)

By Phase 6 the prototype is a real product.

---

## 14. The dovetail with the rest of the fleet

`quilt-port` is the **user-facing gateway** to:

- **`cellforge`** — the AI training substrate (cells, witness chains, dispatcher modes)
- **`moth-corpus`** — the receipted-attack-surface mapping
- **`moth-cells`**, **`moth-honest`**, **`moth-ledger`** — the receipted hunting family
- **`morphic-canvas`** — the GPU substrate
- **`lexical-substrate`** — the bitwise-algebra sibling
- **`mavis-fleet`** — the orchestration spine (now Mavis-multi-tenant)
- **`mavis-substrate-walker`** — the cross-substrate protocol (the Port is a wrapper around the walker)

A user's port can address any subset of these. Most will address one (e.g., a cellforge instance). Power users will address many (their cellforge + their moth collection).

**The port is where the user-meets-fleet boundary gets crossed.** That's the long-term goal, finally concretized.

---

## 15. What's still mysterious (good workshop shape)

We don't yet know:

- Whether the four tiers actually share enough to be one product. (I suspect yes; let's prove it.)
- Whether the cost-plus pricing actually works financially. (Real numbers TBD.)
- Whether the user actually wants one port or several. (Probably one, with quilts.)
- Whether the `.ai` fading is a 1-year phenomenon or 5-year. (Probably 5; hence the no-`.ai` strategy.)
- Whether the IDEATION tier is the wedge that brings in non-developers. (My bet: yes.)
- Whether the long-term fleet governance prevents the ad model from being needed. (TBD.)

These are the questions a workshop should keep *open*.

---

## 16. The next move

I will:

1. **Build the scaffold** at `SuperInstance/quilt-port` on GitHub.
2. **`WORKSHOP.md`** is this doc, ready for round 2 of Casey's edits.
3. **`README.md`** is the public-facing doc — 1-page summary.
4. **`src/quilt_port/port.py`** — the `Port` class with the four projections (Python / Web / ESP32 / Ideation).
5. **`tests/`** — 10 tests, canary preserved at `0x24a555471370b18d`.
6. **`docs/architecture.md`** — diagrams, tier details.

Then we have a place for the conversation to land in code. Iteration happens in `WORKSHOP.md` and the issues. New tiers get added as modules. New revenue models as `quilt_port/billing/*.py`.

---

*This workshop is meant to be done in passes. Each pass sharpens one section, raises new questions in another. The end state is a product that ships — open, honest, and useful to four very different kinds of user.*
