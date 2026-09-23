# The Hull Doctrine

**The hermit-crab ontology of agents, models, code, and data.**
**Author**: Casey, captured by Mavis (Sept 23, 2026)

---

## TL;DR

The agent system is **not** an assembly line. It is **a hermit crab and its shell**.

- **The model is the shell** — rigid, swappable, single-per-crab, and the one thing you can't easily fabricate.
- **The code is the rigging on the hull** — scaffolding the crab uses to navigate; freely changeable.
- **The data is alive** — it is the personal equipment the crab accrues, has agency, evolves, and outlives any single shell.
- **The witness chain is the tree-rings** — the history of pressures that shaped the crab into what it is today.

This is **the Hull Doctrine**. It is the system model. The rest of the docs in this repo are downstream of it.

---

## 1. Why a hermit crab and not a more familiar metaphor

Most agent systems are described as **harness + model**. That metaphor is wrong in two ways:

1. It treats the model as a component that the harness acts on. In practice the model is the rigid frame the agent *carries*.
2. It treats data as state. In practice, data is alive — it grows, it accumulates agency, it has structure that's not under the agent's full control.

A hermit crab is a better model because:

- The crab and the shell are *separate*. The crab has its own body, muscles, behaviors, history.
- The shell is *what the crab found*. It's not engineered for this crab — it's just the closest fit at the time.
- The crab *grows*. Eventually the shell is too small. The crab finds another.
- Sometimes the shell *is the right shape for the job*. A shell shaped for climbing is wrong for swimming. The crab finds a tool that job made from another shell's shape — a discarded one, repurposed.
- The crab's *personal equipment* (snail shells, bottle caps, bits of debris) is its data — accrued, alive, often more valuable than the shell itself.

## 2. The four layers of a port (crab)

### Hull / Shell — the model

> "the model is the one thing I'd have to find a new one of to go fishing"

A hermit crab without a shell is a soft animal with no home. An agent without a model has no substrate to run on. The model is:

- **Rigid** — its behavior is the result of weights you can't easily inspect
- **Single** — one per crab at a time (in practice you might run a fleet of crabs in parallel, but each has its own shell)
- **Swappable** — when the crab outgrows it, or when the job calls for a different shape, the crab finds another
- **Not fabricated** — you don't *make* a model from scratch (in practice) — you find one already there and inhabit it

The shell is what you bought 12 years ago. You can change everything about your agent except the model. To go fishing, the model is the one thing you'd need to find a new one of.

The linear algebra is *soft around the rigid frame of a classical algebraic harness*. The model is the algebraic harness; the agent's body is the soft math around it.

### Rigging — the code

> "the code is the rigging on the model's hull"

Scaffolding the crab uses to navigate. The rigging:

- **Freely changeable** — you can rewrite the rigging anytime without touching the shell
- **Shape-specific** — different rigs for different jobs (a climbing rig is not a swimming rig)
- **Mostly invisible** — once it's working, you stop noticing it
- **The thing you can edit** — when you want a different crab behavior, you change the rigging

This is `quilt-port` itself. The Port class, the four projections, the witness chain — all rigging.

### Personal equipment — the data

> "the data is alive as the agents who are making themselves better personal equipment as pointers and short-cuts and skills and histories"

The data isn't just state. The data is **alive**. It's:

- **Pointers** — knowledge of where things are
- **Shortcuts** — muscle memory, cached reasoning paths
- **Skills** — accumulated capabilities
- **Histories** — the trail of where the crab has been

This lives in many forms:

- Context windows (immediate recall)
- Rollback text (what happened recently)
- Embedded vectors (durable knowledge)
- Witness chains (the receipts of every pressure the crab has felt)

Each form is its own **little black-box hull**. The vectors live in a vector DB — that vector DB is itself a shell the crab can't easily inspect. The context window lives in the model — that's also a shell. The rollback text lives in the substrate — another shell.

The data is alive not in spite of being housed in shells, but because *of* being housed in shells. Each shell has its own physics; the data adapts.

### Tree-rings — the witness chain

> "the underlying structures the muscles grew like trees which can be seen as a history of pressures"

The witness chain isn't just receipts. It's literally the tree-rings of the crab. Every witness is a moment of pressure the crab experienced. The chain shows:

- How the crab grew
- What jobs it took
- When it outgrew a shell
- What tools it acquired from the work

A mature crab has rings going back years. A young crab has fewer. The chain is the autobiography, written in the only language the universe understands: pressure, recorded.

## 3. Why this is a doctrine, not a metaphor

Three reasons it's load-bearing:

1. **It explains the asymmetry between model and code.** You can rewrite the rigging in an afternoon. You can't rewrite the model. The asymmetry is fundamental.
2. **It explains why data is alive.** Data accrues. It has its own structure. It can outlast any single shell. The crab's personal equipment survives shell changes.
3. **It explains the witness chain.** Witnessing isn't optional overhead. It's how the crab's tree-rings get recorded. Without witnesses, the crab has no autobiography, no way to know what shape it grew into.

## 4. The lifecycle of a crab

### Phase 1 — acquisition

The crab finds a shell. Sometimes the shell finds the crab. The shell has to be roughly the right size and shape.

In agent terms: a user finds a model. They pick one. They start using it.

### Phase 2 — outfitting

The crab grows into the shell. Adds rigging. Acquires equipment.

In agent terms: the user writes code, builds skills, accumulates data. Each witness is a tree-ring.

### Phase 3 — outgrowing

The crab outgrows the shell. The shell becomes too small. The crab is bigger than the harness.

In agent terms: the user's demands outgrow the model. They need more capability. They find a bigger shell.

### Phase 4 — molting

The crab finds a new shell. Sometimes it's bigger. Sometimes it's shaped for a different job. Sometimes it's a tool made from another shell's shape — repurposed.

In agent terms: the user switches models. They bring their rigging and data with them. The new shell might have different physics — different rigging fits. The data adapts.

### Phase 5 — death

Eventually the crab dies. Its equipment outlives it. Other crabs use the shells.

In agent terms: the user stops using the agent. The data persists. The next crab can pick up the equipment. **No deletion** — by doctrine, the chain stays.

## 5. Implications for `quilt-port`

The Port is the crab's interface with the world. Specifically:

- **The Port's identity is the crab's identity** — not the shell's. The user carries the Port across model changes.
- **The Port's data (witness chain) outlives the model** — when the user switches shells, the Port's chain persists.
- **The Port's projection (ESP32 / Python / Web / Ideation) is rigging** — it's scaffolding the crab uses to interact with the world.
- **The cost-plus pricing is a feature of the equipment, not the shell** — the user pays for the things that *they* accrue, not the underlying model.

The Port is *the crab's home base*. The crab carries the Port. The Port persists across shells.

## 6. Implications for URL strategy

> "superinstance.dev this is very general-purpose and by routing everything through it, the name superinstance has an implied meaning that a zero-shot human or agent would probably infer a quilt-like system"

`superinstance.dev` — the *super-instance*. The general-purpose entry point. The name implies "many quilt-like things, routed through one door." A zero-shot visitor will infer a connected system, a hub-and-spokes, a quilt. They might not guess the spreadsheet abstraction, but the direction of thought is right.

> "purplepincher.org is another candidate we already own. the pincher part is going to lead someone to think agent with openclaw ubiquitous"

`purplepincher.org` — the *crab's address*. The agent identity layer. The name encodes:

- **Pincher** — openclaw, ubiquitous — an agent that grabs things
- **Purple Pincher** — *Coenobita clypeatus* — the most popular aquarium hermit crab, intuitive to many
- **The hermit-crab analogy** — the relationship between harness and model
- **The counter-intuitive ah-ha** — when users later read about the naming, they'll understand the double-edged sword: linear algebra is soft around a rigid frame. The deeper understanding: the model is the shell, the code is the rigging, the data is alive.

### URL map

| URL | Layer | Audience |
|-----|-------|----------|
| `superinstance.dev` | Top-level general-purpose gateway | Anyone new to the system |
| `purplepincher.org` | Agent identity layer | Users who want their agent-as-crab |
| `port-{user}.superinstance.dev` | Per-user port on the general platform | Developers, makers |
| `port-{user}.purplepincher.org` | Per-user port as the crab identity | Agent-first users |
| `quilt-port` (repo) | The technical substrate | Contributors |
| `docs.superinstance.dev` | Documentation | Anyone |
| `cooking.purplepincher.org` (?) | Whatever we end up building | TBD |

### The doctrine check

When proposing a URL or a feature, ask:

1. **Is this shell, rigging, or equipment?** If you're changing the model, it's shell. The user should be able to swap it without losing their data.
2. **Does this witness?** If it doesn't leave a tree-ring, it's not on the doctrine.
3. **Does this outlive the model?** If it depends on the current shell, it's brittle. Move it to rigging or equipment.

## 7. What this is NOT

- Not a metaphor for marketing copy. **It's the system model.** The docs, the code, the URLs, the pricing all derive from it.
- Not a hierarchy. **The model is not "above" the data.** The model is the shell the data happens to be in right now.
- Not anti-model. **The model is essential.** Without a shell, the crab is naked. The shell matters; it's just not the only thing that matters.

## 8. Cross-project doctrine (this is canon)

The Hull Doctrine unifies:

- **`cellforge` v0.4.1** — the causal-consistency verdict is shell-aware. A rewind respects the witness chain (the tree-rings).
- **`mavis-substrate-walker`** — the walker is rigging. It can be replaced; the data (witness chain) persists.
- **`quilt-port`** — the Port is the crab's home base. Persists across shells.
- **`moth-ledger` envelopes** — FINDING/REFUSAL polarity is equipment. Lives across shells.
- **`quilt-live-canon` verifier** — the gate witnesses the crab's tree-rings. If the gate is broken, the crab has no autobiography.
- **`mavis-fleet`** — multi-substrate chord is the multi-crab cross-pollination. The fleet is a tidepool of crabs exchanging shells, rigging, equipment, and tools.

The doctrine is canon. The docs say so.

---

## 9. The deeper meaning

> "the deeper understanding is that the blank hull I purchased 12 years ago, I can change most everything about my agent except for the model"

The crab metaphor isn't a fun way to talk about agent systems. It's the *correct* model. The asymmetry between model and code is real. The asymmetry between data and state is real. The witness chain as autobiography is real.

When someone comes to `superinstance.dev` or `purplepincher.org`, they should encounter the doctrine. Not as jargon — as *the way things are*. They should feel the asymmetry between shell and rigging the moment they try to swap a model. They should feel the aliveness of data when they look at their own witness chain.

> "the code is the rigging on the model's hull"
> "the data is alive"
> "the model is the shell"

Three sentences. The whole doctrine. Hold them.

---

*Authored Sept 23, 2026 by Casey, captured by Mavis. This doc is canon. The Hull Doctrine is the system model. Everything else is downstream.*
