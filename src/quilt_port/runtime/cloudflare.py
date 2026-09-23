"""Cloudflare Workers runtime — the production target.

Sketch of the Cloudflare Worker entry. Each port becomes a Durable Object.
The DO holds the per-port witness chain. D1 stores port metadata.

This file is a sketch; full implementation lands in Phase 2.

Deployment target:
    wrangler deploy
        name = "quilt-port"
        main = "src/quilt_port/runtime/cloudflare.py:port_worker"
        compatibility_date = "2026-09-01"
        [durable_objects]
        bindings = [{name = "PORT", class_name = "PortDurableObject"}]
        [[d1_databases]]
        binding = "DB"
        database_name = "quilt-port"
        database_id = "<id>"

The Worker entry: serves the OpenAPI surface and routes to the DO per port.
"""
from __future__ import annotations

from typing import Any, Dict, Optional


# This is a sketch — the actual Worker is generated via wrangler templating.
# The shape matches what the CF Worker runtime is expected to provide.

# In production:
#
#   export default {
#     async fetch(request, env, ctx) {
#       const url = new URL(request.url);
#       const port_id = url.pathname.split("/")[2];
#       const id = env.PORT.idFromName(port_id);
#       const stub = env.PORT.get(id);
#       return stub.fetch(request);
#     },
#   };


class PortDurableObject:
    """The Durable Object backing one port.

    Holds:
    - The port's witness chain
    - Per-port cell state
    - Rate-limit counters
    - Pending receipts to sync to D1
    """

    def __init__(self, state: Any, env: Any):
        self.state = state
        self.env = env
        self.user_id: str = ""
        self.projection: str = ""
        self.witnesses: list = []

    async def fetch(self, request) -> Any:
        """Handle a request against this port."""
        # The actual implementation reads from request.method / url / etc.
        # and dispatches to read_cell / write_cell / list_witnesses / etc.
        # The sketch is below; full implementation lands in Phase 2.
        method = getattr(request, "method", "GET")
        url = getattr(request, "url", "/")
        path = url.split("/")[-1] if "/" in url else ""
        return {
            "status": "ok",
            "method": method,
            "path": path,
            "user_id": self.user_id,
            "n_witnesses": len(self.witnesses),
        }
