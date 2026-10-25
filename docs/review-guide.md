# A short review path

1. Read the [PDF case study](pdf-retrieval.md) for an actual diagnosis and bounded repair.
2. Read the [attachment contract](../tasks/attachment/TASK.md), then compare its starter and reference.
3. Inspect [the grader](../grading/test_attachment.py) to see how URL behavior, timeouts, and limits are verified.
4. Run `python bench.py validate` from the repository root.
5. Read [turn ownership](turn-ownership.md) for a design tradeoff and its limits.
6. Read [contribution notes](../CONTRIBUTIONS.md) for attribution and evidence boundaries.

## Suggested interview walkthrough

Explain the user-visible symptom, identify the failing pipeline stage, choose a minimal repair, describe a rejected alternative, and show a test that would fail if the original bug returned. Distinguish the owner's decisions from agent-assisted implementation. Make uncertainty explicit where no measurement exists.

## Current scope

Five small Python repair tasks, complete written contracts, offline smoke tests, behavior-based graders, and reference fixes. This is an inspectable task-design portfolio. There are no claimed production success rates, latency results, agent rankings, or independent research validation.
