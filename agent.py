"""
agent.py — Agentic loop for the Medical Assistant.

Handles multi-turn conversation with tool use, feeding tool results back to
the model until it reaches an end_turn stop reason.

EDUCATIONAL DISCLAIMER: This agent is for educational purposes only and does
not provide medical advice. Always consult a qualified healthcare professional.
"""

from __future__ import annotations

import json
import anthropic

from prompts import SYSTEM_PROMPT
from tools import TOOL_DEFINITIONS, run_tool

# Use claude-opus-4-5 as specified
MODEL = "claude-opus-4-5"
MAX_TOKENS = 4096


def run_agent_turn(
    client: anthropic.Anthropic,
    conversation_history: list[dict],
) -> tuple[str, dict | None]:
    """
    Run a single agent turn: send the current conversation history to the model,
    process any tool calls in a loop, and return when stop_reason == 'end_turn'.

    Args:
        client:               Anthropic API client.
        conversation_history: Full message history (user + assistant turns).

    Returns:
        Tuple of (assistant_text_response, report_dict_or_None).
        report_dict is populated if the generate_report tool was called.
    """
    report: dict | None = None
    assistant_text_parts: list[str] = []

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            tools=TOOL_DEFINITIONS,
            messages=conversation_history,
        )

        # Collect text content from this response
        for block in response.content:
            if block.type == "text":
                assistant_text_parts.append(block.text)

        # Append the raw assistant message to history
        conversation_history.append(
            {"role": "assistant", "content": response.content}
        )

        # If the model is done, exit the loop
        if response.stop_reason == "end_turn":
            break

        # Handle tool_use stop_reason
        if response.stop_reason == "tool_use":
            tool_results = []

            for block in response.content:
                if block.type != "tool_use":
                    continue

                tool_name = block.name
                tool_input = block.input
                tool_use_id = block.id

                print(f"\n[Agent] Calling tool: {tool_name}")
                result_json = run_tool(tool_name, tool_input)
                result_data = json.loads(result_json)

                # Capture the report if it was generated
                if tool_name == "generate_report":
                    report = result_data

                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,
                        "content": result_json,
                    }
                )

            # Feed all tool results back as a user message
            conversation_history.append(
                {"role": "user", "content": tool_results}
            )
            # Continue the loop — model will process results and respond
        else:
            # Unexpected stop reason; exit gracefully
            break

    assistant_text = "\n".join(assistant_text_parts).strip()
    return assistant_text, report


def create_client() -> anthropic.Anthropic:
    """Instantiate and return the Anthropic client."""
    return anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from environment
