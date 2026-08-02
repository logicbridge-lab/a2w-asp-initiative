# A2W/ASP Reference Agent — Design Specification

## Overview

A lightweight Playwright-based browser agent for benchmarking ASP-guided vs raw web navigation. The agent is intentionally simple: it uses heuristic + LLM-assisted decision making to choose actions, but does not implement complex planning, memory, or recovery. Its purpose is to provide a consistent, reproducible baseline for the benchmark harness.

## Modes

### Raw Web Mode
- No ASP available
- Agent must infer page structure, forms, and actions from DOM
- Uses generic heuristics: visible text, form fields, link text, button labels
- LLM prompt includes only the goal and current page snapshot

### ASP-Guided Mode
- ASP Draft loaded for the target domain
- Agent receives relevant ASP sections for current page: resources, actions, policies, workflows
- LLM prompt includes goal, current page snapshot, and ASP guidance
- Policies enforced as hard constraints (agent must not attempt prohibited actions)

## Agent Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      ReferenceAgent                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Browser    │  │  Extractor  │  │  Decision Engine    │  │
│  │  (Playwright)│  │  (DOM +     │  │  (Heuristic +       │  │
│  │             │  │   Screenshot)│  │   LLM)              │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         │                │                     │             │
│         └────────────────┼─────────────────────┘             │
│                          ▼                                   │
│              ┌─────────────────────┐                         │
│              │  Action Executor    │                         │
│              │  (click, type, nav) │                         │
│              └─────────────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

## Decision Engine

### Input
- Goal: natural language task description
- Page snapshot: simplified DOM + optional screenshot
- ASP context (ASP-guided mode only): relevant actions, resources, policies for current URL

### Heuristic Scoring (Raw Web)
For each interactive element, compute a relevance score:
- Text similarity to goal keywords (TF-IDF or embedding)
- Element type priority: form submit > button > link > input
- Visibility and interactability
- Position (above fold preferred)

### LLM Prompt (Both Modes)
```
You are a web navigation agent. Your goal: {goal}

Current page: {url}
Page snapshot: {simplified_dom}

{asp_context_if_available}

Available actions (choose ONE):
1. CLICK <selector> - Click an element
2. TYPE <selector> <text> - Type into an input
3. NAVIGATE <url> - Go to a URL
4. WAIT <ms> - Wait for dynamic content
5. DONE - Goal achieved
6. FAIL - Cannot proceed

Respond with JSON: {"action": "CLICK", "selector": "...", "reasoning": "..."}
```

### ASP Context Injection
When ASP is available, include:
```
ASP Guidance for {url}:
Resources: {relevant_resources}
Actions: {relevant_actions_with_params}
Policies: {applicable_policies}
Workflow hint: {next_workflow_step_if_any}
```

### Policy Enforcement
Before executing any action, check against ASP policies:
- Prohibitions: reject action if matches prohibited pattern
- Rate limits: track request timestamps per domain
- Auth requirements: ensure credentials available before authenticated actions

## Action Space

| Action | Parameters | Description |
|--------|------------|-------------|
| CLICK | selector (CSS) | Click element |
| TYPE | selector, text | Type into input/textarea |
| NAVIGATE | url | Direct navigation |
| WAIT | ms | Wait for network idle or timeout |
| SCROLL | direction | Scroll page |
| DONE | — | Signal goal completion |
| FAIL | reason | Signal inability to proceed |

## Logging

Every decision and action logged as JSONL:
```json
{
  "timestamp": "2026-08-01T12:00:00Z",
  "task_id": "restaurant-001",
  "mode": "asp_guided",
  "step": 3,
  "url": "https://example.com/book",
  "goal": "Book a table for 2 at 7pm",
  "decision": {"action": "TYPE", "selector": "#date", "text": "2026-08-15", "reasoning": "ASP action book_appointment requires date parameter"},
  "asp_context_used": true,
  "policy_check": {"checked": "prohibitions", "result": "pass"},
  "result": {"success": true, "new_url": "https://example.com/book"}
}
```

## Verification Interface

The agent exposes a `verify(goal, page)` method that the harness calls to check task completion. For the pilot tasks, verification is implemented as:
- Restaurant: page contains time slot matching "today" + "available"
- Government: page contains downloadable PDF link with "permit" in title
- E-commerce: cart page shows target product name
- Healthcare: page contains phone regex + hours for target day
- Documentation: page contains code block in auth section
- University: page contains date + program name "Computer Science"

## Configuration

```python
@dataclass
class AgentConfig:
    mode: Literal["raw", "asp_guided"]
    headless: bool = True
    timeout_ms: int = 30000
    max_steps: int = 20
    llm_model: str = "hf.co/HuggingFaceTB/SmolLM2-1.7B-Instruct-GGUF"
    llm_temperature: float = 0.1
    screenshot_on_step: bool = False
```

## Dependencies

- playwright >= 1.40
- huggingface-hub (for GGUF model download)
- llama-cpp-python or ollama (for local LLM inference)
- pydantic (for config/validation)
- jsonschema (for ASP validation)

## Files

```
benchmark/
├── agents/
│   ├── __init__.py
│   ├── reference_agent.py      # Main agent class
│   ├── decision_engine.py      # Heuristic + LLM decision logic
│   ├── dom_extractor.py        # DOM simplification + element detection
│   ├── asp_context.py          # ASP loading + relevance filtering
│   ├── policy_enforcer.py      # Policy checking
│   └── verification.py         # Task verification predicates
├── src/
│   ├── harness.py              # Benchmark runner
│   ├── metrics.py              # Metrics computation
│   └── tasks.py                # Task definitions loader
└── tasks/
    └── pilot_tasks.jsonl       # 6 pilot tasks
```