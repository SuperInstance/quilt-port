"""Web projection — REST + OpenAPI 3.1.

Surface:
- GET /v1/cells/{cell_id} -> JSON cell
- POST /v1/cells/{cell_id} -> JSON cell
- GET /v1/quilts/{quilt_id}/witnesses -> chain (paginated)
- POST /v1/quilts/{quilt_id}/promote -> {finding_id, content_hash}

Wire format: JSON over HTTPS.
Trust: bearer token.
Latency budget: 500ms.

The OpenAPI spec is generated from this module via:
    python -c "from quilt_port.projections.web import openapi_spec; print(openapi_spec())"
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from ..port import Port


async def read_cell_http(port: Port, cell_id: str) -> Dict[str, Any]:
    """REST-shaped response for a cell read."""
    return {
        "cell_id": cell_id,
        "port_id": port.port_id,
        "value": None,  # populated by the runtime
        "witness": {
            "kind": "walk",
            "substrate_id": f"port_{port.user_id}",
        },
    }


async def write_cell_http(port: Port, cell_id: str, payload: Dict[str, Any],
                          quilt: Optional[str] = None) -> Dict[str, Any]:
    """REST-shaped response for a cell write."""
    return {
        "cell_id": cell_id,
        "port_id": port.port_id,
        "quilt": quilt or "<auto>",
        "received": True,
        "witness": {
            "kind": "stitch",
            "substrate_id": f"port_{port.user_id}",
        },
    }


async def list_witnesses_http(port: Port, quilt_id: str, page: int = 0, size: int = 50
                              ) -> Dict[str, Any]:
    """REST-shaped paginated witness listing."""
    chain = port.witness_chain
    start = page * size
    end = start + size
    items = [
        {
            "content_hash": w.content_hash,
            "kind": w.kind.value,
            "timestamp": w.timestamp,
            "payload": w.payload,
        }
        for w in chain.witnesses[start:end]
    ]
    return {
        "quilt_id": quilt_id,
        "page": page,
        "size": len(items),
        "total": chain.size(),
        "items": items,
    }


async def promote_http(port: Port, quilt_id: str) -> Dict[str, Any]:
    """REST-shaped promotion response."""
    return {
        "quilt_id": quilt_id,
        "promoted": False,  # v0.1 stub
        "n_witnesses": port.witness_chain.size(),
        "reason": "v0.1-stub: real promotion gate (JEV p>0.7) lands in Phase 1.5",
    }


def openapi_spec() -> Dict[str, Any]:
    """Generate the OpenAPI 3.1 spec for the Web projection."""
    return {
        "openapi": "3.1.0",
        "info": {
            "title": "quilt-port",
            "version": "0.1.0",
            "description": (
                "REST + OpenAPI surface for quilt-port. Same canon as the "
                "Python projection; same witness chain; different access surface."
            ),
        },
        "servers": [
            {"url": "https://port.workers.dev/v1", "description": "Hosted (Cloudflare Workers)"},
        ],
        "paths": {
            "/cells/{cell_id}": {
                "get": {
                    "summary": "Read a cell",
                    "parameters": [{"name": "cell_id", "in": "path", "required": True, "schema": {"type": "string"}}],
                    "responses": {"200": {"description": "Cell + witness"}},
                },
                "post": {
                    "summary": "Write a cell",
                    "parameters": [{"name": "cell_id", "in": "path", "required": True, "schema": {"type": "string"}}],
                    "requestBody": {"required": True, "content": {"application/json": {"schema": {"type": "object"}}}},
                    "responses": {"200": {"description": "Receipt"}},
                },
            },
            "/quilts/{quilt_id}/witnesses": {
                "get": {
                    "summary": "List witnesses on a quilt",
                    "parameters": [
                        {"name": "quilt_id", "in": "path", "required": True, "schema": {"type": "string"}},
                        {"name": "page", "in": "query", "schema": {"type": "integer", "default": 0}},
                        {"name": "size", "in": "query", "schema": {"type": "integer", "default": 50}},
                    ],
                    "responses": {"200": {"description": "Paginated witness chain"}},
                },
            },
            "/quilts/{quilt_id}/promote": {
                "post": {
                    "summary": "Graduate a chain to a canonical finding",
                    "parameters": [{"name": "quilt_id", "in": "path", "required": True, "schema": {"type": "string"}}],
                    "responses": {"200": {"description": "Promotion response"}},
                },
            },
        },
        "components": {
            "securitySchemes": {
                "bearerAuth": {"type": "http", "scheme": "bearer"},
            },
        },
    }
