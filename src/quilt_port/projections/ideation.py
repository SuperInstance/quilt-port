"""Ideation projection — chat-driven, AI-Writings integrated.

Surface (sketch):
- User chats: 'give me the receipt for last night's run'
- Each chat turn is a witness
- The user's canon accrues from each exploration
- AI-Writings front-end integration (a separate repo)
- Async; latency is not strict

For v0.1 we keep the projection minimal — the chat is async, witnessing
the dialogues, and the diamond-mining happens at the user's pace.
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, AsyncIterator, Dict, List, Optional

from ..port import Port
from .._vendor.mavis_substrate_walker import Witness, WitnessKind


@dataclass
class ChatTurn:
    """One turn in the ideation chat."""
    text: str
    attached_witness: Optional[Dict[str, Any]] = None
    role: str = "assistant"  # 'user' or 'assistant'


class IdeationPort:
    """The chat-driven projection of a Port.

    Each chat turn is a witness on the port's chain. The user can read the
    canon they've accrued by asking for receipts.

    Example:
        chat = IdeationPort(projection="ideation", user_id="casey")
        async for turn in chat.stream("give me the receipt for last night's run"):
            print(turn.text, turn.attached_witness)
    """

    def __init__(self, user_id: str, projection: str = "ideation",
                 quilts: Optional[List[str]] = None,
                 endpoint: str = "https://port.workers.dev"):
        # Lazy import to avoid pulling in all of Port when not used.
        from ..port import Port as _Port, Projection as _Projection
        self.port = _Port(
            user_id=user_id,
            projection=_Projection(projection),
            quilts=quilts or [],
            endpoint=endpoint,
        )
        # A simple in-memory dialogue log
        self.dialogue: List[ChatTurn] = []

    async def stream(self, prompt: str) -> AsyncIterator[ChatTurn]:
        """Stream a chat response. Each turn is witnessed.

        In v0.1, this is a stub that returns a single canned response.
        Phase 4 wires it to the AI-Writings chat backend.
        """
        self.dialogue.append(ChatTurn(text=prompt, role="user"))
        # Witness the user's prompt
        self.port.emit_witness_sync(
            kind=WitnessKind.WALK,
            payload={"projection": "ideation", "op": "user_prompt", "text": prompt[:200]},
        )

        # Generate the assistant response (v0.1 stub).
        n = self.port.witness_chain.size()
        response_text = (
            f"[v0.1-stub] I'm your {self.port.projection.value}-tier port. "
            f"You asked: {prompt!r}. "
            f"Your port has accrued {n} witnesses so far."
        )
        self.dialogue.append(ChatTurn(text=response_text, role="assistant"))

        # Witness the assistant's response
        w = self.port.emit_witness_sync(
            kind=WitnessKind.WALK,
            payload={"projection": "ideation", "op": "assistant_response", "text": response_text[:200]},
        )
        yield ChatTurn(
            text=response_text,
            attached_witness={"content_hash": w.content_hash, "kind": w.kind.value},
            role="assistant",
        )
