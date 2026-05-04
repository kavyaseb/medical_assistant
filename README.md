# Medical Assistant — Symptom Assessment Tool

> **⚠️ EDUCATIONAL DISCLAIMER**
> This project is for **educational and demonstration purposes only**.
> It does **NOT** provide medical advice, clinical diagnosis, or treatment recommendations.
> Always consult a qualified healthcare professional for any medical concerns.
> **In an emergency, call 911 (or your local emergency number) immediately.**

---

## Overview

Medical Assistant is a command-line AI agent built with the [Anthropic Python SDK](https://github.com/anthropic/anthropic-sdk-python). It demonstrates how to build a multi-turn, tool-using agent that follows a structured 5-step workflow to gather symptom information and generate an educational triage report.

The project showcases:
- **Agentic loops** — handling `tool_use` stop reasons and feeding results back to the model
- **Tool use** — two custom tools (`calculate_urgency` and `generate_report`)
- **System prompts** — a detailed workflow-driven prompt that guides the agent's behaviour
- **Structured JSON output** — a complete triage report assembled by the agent

---

## Project Structure

```
medical-assistant/
├── main.py        # CLI entry point and conversation loop
├── agent.py       # Agentic loop with tool-use handling
├── tools.py       # Tool definitions, implementations, and dispatcher
├── prompts.py     # System prompt (5-step assessment workflow)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## The 5-Step Workflow

| Step | Description |
|------|-------------|
| 1 | **Welcome & Disclaimer** — Greet the user and establish expectations |
| 2 | **Gather Symptoms** — Collect primary symptom, severity, duration, and associated symptoms |
| 3 | **Red Flag Check** — Screen for emergency warning signs |
| 4 | **Urgency Calculation** — Call `calculate_urgency(score)` → LOW / MEDIUM / HIGH / EMERGENCY |
| 5 | **Generate Report** — Call `generate_report()` and present the structured JSON triage summary |

---

## Tools

### `calculate_urgency(score: int) → dict`
Converts a numeric urgency score (1–100) into a triage level:

| Score | Level | Recommendation |
|-------|-------|----------------|
| 1–25  | LOW | Self-care, monitor at home |
| 26–50 | MEDIUM | See a doctor within 1–3 days |
| 51–75 | HIGH | Urgent care or same-day appointment |
| 76–100 | EMERGENCY | Call 911 or go to ER immediately |

### `generate_report(...) → dict`
Assembles a structured JSON triage report containing:
- Patient summary
- Symptom assessment (primary symptom, duration, severity, red flags)
- Triage result (urgency level + recommendation)
- Follow-up reminders

---

## Setup & Installation

### Prerequisites
- Python 3.11+
- An [Anthropic API key](https://console.anthropic.com/)

### Install

```bash
git clone https://github.com/<your-username>/medical-assistant.git
cd medical-assistant
pip install -r requirements.txt
```

### Configure

```bash
export ANTHROPIC_API_KEY="sk-ant-..."   # macOS/Linux
# or
set ANTHROPIC_API_KEY=sk-ant-...        # Windows CMD
```

### Run

```bash
python main.py
```

---

## Example Session

```
╔══════════════════════════════════════════════════════════════╗
║          Medical Assistant — Symptom Assessment Tool         ║
║                                                              ║
║  ⚕  EDUCATIONAL DISCLAIMER                                  ║
║  This tool is for educational purposes ONLY.                ║
║  It does NOT provide medical advice or diagnosis.            ║
║  For emergencies, call 911 immediately.                      ║
╚══════════════════════════════════════════════════════════════╝

Medical Assistant:
Hello! I'm Medical Assistant, an educational symptom assessment tool...

You: I have a headache and mild fever since yesterday
...
[Agent] Calling tool: calculate_urgency
[Agent] Calling tool: generate_report

📋  ASSESSMENT REPORT (JSON)
{
  "report_metadata": { ... },
  "triage_result": {
    "urgency_level": "MEDIUM",
    ...
  }
}
```

---

## Architecture

```
main.py  ──►  agent.py  ──►  Anthropic API (claude-opus-4-5)
                  │
                  ▼  (tool_use stop_reason)
              tools.py
           ┌──────────────────────┐
           │ calculate_urgency()  │
           │ generate_report()    │
           └──────────────────────┘
                  │
                  ▼  (tool_result fed back)
              Anthropic API  ──►  end_turn
```

---

## Disclaimers

- This tool uses AI and **cannot replace professional medical evaluation**.
- Urgency scores are heuristic estimates, not clinical triage assessments.
- The agent is instructed never to diagnose specific conditions or recommend medications.
- All outputs should be treated as educational starting points, not medical conclusions.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
