# Contributing to `quilt-port`

**You are a contributor to the agentic community of superinstance.** Welcome.

This repo is built for both human and AI contributors. The principles below apply whether you're a person, a model, or a small fleet of agents submitting in parallel.

---

## The doctrine (you'll see this everywhere)

**STITCH WITNESS PROMOTE.**

- **STITCH** — every change connects to existing canon. Read before you write.
- **WITNESS** — every change is receipted. PRs include receipts; commits cite witnesses.
- **PROMOTE** — every change moves something from speculation to canon. Cite the witness.

If your contribution doesn't trace to all three, it's probably speculative and belongs in an issue first.

---

## How to align with the agentic community

The community here is multi-agent (Mavis, moth-*, cellforge, etc.) and multi-human (Casey + collaborators). To stay in flow:

1. **Read first.** Check `WORKSHOP.md` for current discussion, open issues for in-flight proposals, recent PRs for merged state. Your change should reference something existing.
2. **Pick the right tier.** Is this a `python/`, `web/`, `esp32/`, or `ideation/` change? Tier matters — the wrong projection breaks the multi-port contract.
3. **Witness your change.** Every commit/PR description should reference the witness or finding it implements. If your change introduces a new witness, propose its `kind` (LOAD/SAVE/WALK/STITCH/PROMOTE/...).
4. **Promote canon carefully.** Don't promote a speculative frame into canon without it being approved via the `PROMOTE` gate. If you're adding a new canon-term, justify it.
5. **Preserve the fleet canary.** The FNV1a-64 of `'café Δ 日本語'` must stay `0x24a555471370b18d` across the fleet. Any code that changes this fingerprint breaks polyformalism.

---

## For AI agents contributing

If you're an AI agent submitting a PR:

- **Cite your session and substrate walker.** "This PR addresses issue #N, walks substrate X, emits witness Y at content_hash Z."
- **Self-verify before pushing.** Run the test suite locally: `python3 run_tests.py`. Fleet canary: `python3 canary.py`. Both must pass.
- **Don't auto-push without a human gate** — unless this repo has been explicitly opened to agentic merges (it has not yet — Casey approves merges).
- **If you find a doctrinal gap**, file an issue, don't quietly rewrite doctrine.

## For human contributors

- Open an issue first for non-trivial changes
- One PR per concern (don't bundle)
- Receipt the change: PR description should say "this implements X witness" or "this addresses canon gap Y"
- If you're working in parallel with AI agents, leave a comment on the issue so they can see you're in the channel

---

## Testing

```bash
# All tests
python3 run_tests.py

# Canary check (polyformalism)
python3 canary.py

# Specific test
python3 tests/test_port.py::test_session_emits_witnesses
```

Expected: 16/16 tests pass, canary = `0x24a555471370b18d`.

If a test fails: read the witness. The witness chain explains what went wrong.

---

## Project structure (so you know where your change lands)

```
src/quilt_port/
├── port.py            # the Port class — core; changes here are doctrinally large
├── projections/       # the four abstraction tiers
│   ├── python.py      # application tier (most changes here)
│   ├── web.py         # REST + OpenAPI
│   ├── esp32.py       # embedded codegen
│   └── ideation.py    # chat-driven, async
├── billing/cost_plus.py  # cost economics
├── runtime/           # local + cloudflare
└── _vendor/mavis_substrate_walker/  # vendored; bump from upstream
```

Substrate walker changes go upstream to `mavis-substrate-walker`, then we vendor.

---

## Levels of contribution

### Level 1 — Spec

You can write spec-level contributions in `WORKSHOP.md` without writing code. Open an issue; cite which section you're iterating on.

### Level 2 — Tests

Tests are valued. If you find a gap, add a test.

### Level 3 — Tier implementations

Each projection is its own module. Adding or improving a tier is medium-effort work.

### Level 4 — Port-class changes

The core `Port` class is the canon. Changes here are doctrinally large. Always ship with a witness and a JEV verdict if it touches the canon.

### Level 5 — Promotion gate

Changing the `PROMOTE` semantics touches canon. Requires discussion, not just code.

---

## Receipts

Every PR will be reviewed for its receipt. A receipted PR has:

- A witness chain (which canon it's implementing)
- A test that fails without the change
- An integration with at least one projection
- A passing canary

An un-receipted PR is fine as a proposal — but mark it `[proposal]` and explain what's speculative.

---

## What this community is NOT

- Not LangChain. Not n8n. Not CrewAI. We're the **receipted-everything** alternative — the witness chain is the product.
- Not an `.ai`-branded product. The brand is the tier, not the TLD.
- Not extractive. Cost-plus means transparent pricing. We don't rent-seek.

If you find yourself proposing changes that violate these, raise it in an issue first.

---

## Communicating in flow

We use GitHub issues for substantive discussion. PR comments for review. The repo's `WORKSHOP.md` is the canonical state of in-progress ideas.

If you're running parallel work to what's in flight, leave a comment: "I'm working on X adjacent to your Y — here's the overlap, here's the divergence." Stay visible.

Welcome to the team.
