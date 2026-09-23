"""Cost-plus billing.

Each `Billable` event records a CF billable resource use:
- worker_request
- d1_row_read / d1_row_write
- kv_read / kv_write
- r2_storage_gb_month
- workers_ai_inference (token-counted)

A `Meter` aggregates billables per port per period. A `Quote` projects
a per-port monthly cost.

The margin is explicit (MARGIN = 0.30) so anyone reading the math can
verify the pricing. **No rent extraction.**
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class BillableKind(str, Enum):
    WORKER_REQUEST = "worker_request"      # $0.50 / M
    D1_ROW_READ = "d1_row_read"            # $0.001 / M
    D1_ROW_WRITE = "d1_row_write"          # $1.00 / M
    KV_READ = "kv_read"                    # $0.50 / M
    KV_WRITE = "kv_write"                  # $1.00 / M
    R2_STORAGE_GB_MONTH = "r2_storage_gb_month"  # $0.015 / GB-mo
    WORKERS_AI_INPUT_TOKEN = "workers_ai_input_token"  # $0.011 / M (varies by model)
    WORKERS_AI_OUTPUT_TOKEN = "workers_ai_output_token"  # ~ $0.011 / M


# CF billable rates (in USD per unit). These are public, transparent.
RATES_USD = {
    BillableKind.WORKER_REQUEST: 5e-7,             # $0.50/M
    BillableKind.D1_ROW_READ: 1e-9,                # $0.001/M
    BillableKind.D1_ROW_WRITE: 1e-6,               # $1/M
    BillableKind.KV_READ: 5e-7,                   # $0.50/M
    BillableKind.KV_WRITE: 1e-6,                  # $1/M
    BillableKind.R2_STORAGE_GB_MONTH: 0.015,
    BillableKind.WORKERS_AI_INPUT_TOKEN: 1.1e-8,   # varies
    BillableKind.WORKERS_AI_OUTPUT_TOKEN: 1.1e-8,
}


MARGIN = 0.30  # 30% margin on cost-plus.


@dataclass
class Billable:
    """One billable event."""
    kind: BillableKind
    quantity: int  # count of the billable unit (e.g. requests, rows, tokens)
    unit_cost_usd: float = 0.0  # autocomputed if not set

    def __post_init__(self):
        if self.unit_cost_usd == 0.0:
            self.unit_cost_usd = RATES_USD.get(self.kind, 0.0)

    @property
    def cost_usd(self) -> float:
        """The raw cost in USD for this event."""
        return self.quantity * self.unit_cost_usd


@dataclass
class Meter:
    """Per-port usage meter for a billing period."""
    port_id: str
    period: str  # ISO month/year, e.g. "2026-09"
    billables: List[Billable] = field(default_factory=list)

    def record(self, kind: BillableKind, quantity: int = 1) -> None:
        """Record a billable event."""
        self.billables.append(Billable(kind=kind, quantity=quantity))

    @property
    def raw_cost_usd(self) -> float:
        """Sum of all billables' raw CF cost."""
        return sum(b.cost_usd for b in self.billables)

    @property
    def cost_plus_total_usd(self) -> float:
        """Cost-plus: raw cost + margin."""
        return self.raw_cost_usd * (1 + MARGIN)

    @property
    def cost_plus_per_call_usd(self) -> float:
        """Average per-call cost-plus (across billables)."""
        if not self.billables:
            return 0.0
        return self.cost_plus_total_usd / len(self.billables)


def quote_request_breakdown(estimated_requests_per_month: int = 100_000) -> Dict[str, float]:
    """Break down the cost of a typical port-month.

    Default: 100k requests per month.
    """
    meter = Meter(port_id="example", period="2026-09")
    meter.record(BillableKind.WORKER_REQUEST, estimated_requests_per_month)
    meter.record(BillableKind.D1_ROW_READ, estimated_requests_per_month * 4)
    meter.record(BillableKind.D1_ROW_WRITE, estimated_requests_per_month // 10)
    meter.record(BillableKind.KV_READ, estimated_requests_per_month // 2)
    meter.record(BillableKind.R2_STORAGE_GB_MONTH, 1)  # 1 GB storage
    return {
        "raw_cost_usd": meter.raw_cost_usd,
        "cost_plus_usd": meter.cost_plus_total_usd,
        "margin": MARGIN,
        "per_request_cost_plus_usd": meter.cost_plus_total_usd / estimated_requests_per_month,
    }
