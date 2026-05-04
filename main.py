"""
main.py — CLI entry point for the Medical Assistant.

EDUCATIONAL DISCLAIMER: This application is for educational and informational
purposes only. It does NOT provide medical advice, diagnosis, or treatment
recommendations. Always consult a qualified healthcare professional for any
medical concerns. In an emergency, call 911 or your local emergency number
immediately.
"""

from __future__ import annotations

import json
import sys

from agent import create_client, run_agent_turn

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║          Medical Assistant — Symptom Assessment Tool         ║
║                                                              ║
║  ⚕  EDUCATIONAL DISCLAIMER                                  ║
║  This tool is for educational purposes ONLY.                ║
║  It does NOT provide medical advice or diagnosis.            ║
║  For emergencies, call 911 immediately.                      ║
╚══════════════════════════════════════════════════════════════╝
"""

EXIT_COMMANDS = {"exit", "quit", "bye", "q"}


def print_separator() -> None:
    print("\n" + "─" * 66 + "\n")


def main() -> None:
    print(BANNER)

    client = create_client()
    conversation_history: list[dict] = []
    final_report: dict | None = None

    # Kick off the conversation with an empty user message so the agent greets first
    conversation_history.append(
        {"role": "user", "content": "Hello, I need help assessing my symptoms."}
    )

    print("Type 'exit' or 'quit' at any time to end the session.\n")

    while True:
        # Run the agent turn (may involve multiple tool calls internally)
        assistant_response, report = run_agent_turn(client, conversation_history)

        if report:
            final_report = report

        print_separator()
        print(f"Medical Assistant:\n{assistant_response}")
        print_separator()

        # If a report was just generated, display it and offer to exit
        if report:
            print("\n📋  ASSESSMENT REPORT (JSON)\n")
            print(json.dumps(report, indent=2))
            print(
                "\n──────────────────────────────────────────────────────────────\n"
                "REMINDER: The report above is for educational purposes only.\n"
                "Please consult a qualified healthcare professional.\n"
                "──────────────────────────────────────────────────────────────\n"
            )

        # Prompt the user for their next message
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nSession ended. Stay healthy!")
            break

        if not user_input:
            continue

        if user_input.lower() in EXIT_COMMANDS:
            print("\nThank you for using Medical Assistant. Please remember to consult")
            print("a qualified healthcare professional for any medical concerns.")
            print("Stay healthy! 👋\n")
            break

        # Append the user's message and continue
        conversation_history.append({"role": "user", "content": user_input})

    # If a report was generated, offer to save it
    if final_report:
        try:
            save = input("\nWould you like to save the report to a file? (y/n): ").strip().lower()
            if save == "y":
                filename = "assessment_report.json"
                with open(filename, "w") as f:
                    json.dump(final_report, f, indent=2)
                print(f"Report saved to {filename}")
        except (EOFError, KeyboardInterrupt):
            pass

    sys.exit(0)


if __name__ == "__main__":
    main()
