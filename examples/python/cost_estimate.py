"""Cost estimator — what does your port-month cost?"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from quilt_port.billing.cost_plus import quote_request_breakdown


def main():
    print("quilt-port — cost-plus pricing estimator")
    print("=" * 50)
    print()

    for monthly in [1_000, 10_000, 100_000, 1_000_000, 10_000_000]:
        b = quote_request_breakdown(estimated_requests_per_month=monthly)
        print(f"{monthly:>10,} requests/mo:")
        print(f"  raw cost     ${b['raw_cost_usd']:.6f}")
        print(f"  cost-plus    ${b['cost_plus_usd']:.6f}  (margin {b['margin']:.0%})")
        print(f"  per request  ${b['per_request_cost_plus_usd']:.10f}")
        print()


if __name__ == "__main__":
    main()
