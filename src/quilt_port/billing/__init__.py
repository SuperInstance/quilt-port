"""Billing model — cost-plus pricing.

The doctrine:
- We charge what it costs us to run, plus a fair margin (~30%).
- We never compete by lock-in; we compete by hosting convenience.
- Anyone can fork, deploy their own CF Worker, run their own cost-plus stack.

This module computes per-port cost from raw CF billable events.
A `Meter` records usage; a `Quote` projects cost.
"""
from . import cost_plus
