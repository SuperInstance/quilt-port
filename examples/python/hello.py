"""Hello quilt-port — Python projection."""
import asyncio
import sys
from pathlib import Path

# Allow running from the repo root
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from quilt_port import Port, Projection


async def main():
    # Create a Port. user_id is the user's identity; projection is the tier.
    port = Port(
        user_id="alice",
        projection=Projection.PYTHON,
        quilts=["alice-ledger"],
    )

    print(f"Port: {port}")
    print(f"Port ID: {port.port_id}")
    print(f"Witness chain substrate: port_{port.user_id}")
    print()

    # Open a session. Every operation is witnessed.
    async with port.session() as session:
        # Read a cell.
        cell = await session.cell("weights/dense")
        print(f"Read cell: {cell}")

        # Record an observation.
        receipt = await session.record({"step": 1, "weight": 0.42})
        print(f"Recorded: {receipt.content_hash[:16]}...")
        print(f"  tier: {receipt.tier.value}")
        print(f"  op:   {receipt.operation}")
        print()

        # Another record.
        receipt2 = await session.record({"step": 2, "weight": 0.39})
        print(f"Recorded: {receipt2.content_hash[:16]}...")

        # Promote the chain to a canonical finding.
        promo = await session.promote()
        print(f"Promoted: {promo.content_hash[:16]}...")
        print()

    # Verify the chain.
    if port.witness_chain_verify():
        print("✓ Witness chain verified intact.")
    else:
        print("✗ Chain broke!")

    print(f"Total witnesses: {port.witness_chain.size()}")
    for i, w in enumerate(port.witness_chain.witnesses):
        print(f"  [{i}] {w.kind.value:8s}  {w.content_hash[:16]}...  payload={dict(w.payload)}")


if __name__ == "__main__":
    asyncio.run(main())
