---
name: ⚓ Witness — receipt a finding
about: Report a finding that should graduate to canon
title: "[witness] "
labels: ["witness", "canon-candidate"]
---

## What I found

State the finding in 1-2 sentences.

## The witness

What is the receipt? It could be:
- A test that fails without the change
- A measurement with reproducible code
- A canonical hash chain that verifies
- A port receipt (from `quilt-port`)

## Chain anchors

Which existing canon does this witness anchor to? Cite `kind`, `content_hash`, or canonical reference.

## Promotion gate

What should trigger `PROMOTE` here?
- JEV p > 0.7 (default)
- Cost-plus "this tier transitions to that tier" rules
- Manual review by maintainer

---

### What happens next

A witness is a *findable, falsifiable claim*. Community will:

1. Try to reproduce (the re-derive)
2. Try to falsify (the adversary pass)
3. Either promote (move to canon) or refute

Receipted witnesses that survive promote to canon.
