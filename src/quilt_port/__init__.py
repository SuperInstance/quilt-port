"""quilt-port — the user's port to their quilts.

A Port is one user identity with the Quilt. It addresses one or many quilts.
It carries four projections: ESP32, Python, Web, Ideation.

Doctrine:
- STITCH (load a quilt, save the witness back)
- WITNESS (emit a receipt for every step)
- PROMOTE (graduate a chain to a canonical finding)

The Port wraps the substrate walker (mavis-substrate-walker) with
multi-tenancy and projection layers. Receipts at every step.
"""
from __future__ import annotations

from .port import Port, PortSession, PortReceipt, Projection
from .projections import esp32, python, web, ideation
from .billing import cost_plus
from .runtime import cloudflare, local

__version__ = "0.1.0"
__all__ = [
    "Port",
    "PortSession",
    "PortReceipt",
    "Projection",
    # Projections
    "esp32",
    "python",
    "web",
    "ideation",
    # Billing
    "cost_plus",
    # Runtime
    "cloudflare",
    "local",
]
