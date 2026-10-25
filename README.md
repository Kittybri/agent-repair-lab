# Conversational Agent Repair Lab

Five reproducible Python repair tasks inspired by failures encountered while developing [Scaramouche](https://github.com/Kittybri/Scaramouche) and [Wanderer](https://github.com/Kittybri/Wanderer).

This repository demonstrates task design, behavioral grading, failure reproduction, and reference fixes. It contains no agent leaderboard, cost measurements, latency study, or model-comparison results.

## Try a task

Python 3.11 or newer; standard library only. No Discord account, API key, GPU, or paid service is required.

For a short synthetic walkthrough, run `python demo.py`. It demonstrates the five reference contracts without contacting a model or Discord.

```sh
git clone https://github.com/Kittybri/agent-repair-lab.git
cd agent-repair-lab
python bench.py prepare attachment ../attachment-workspace
```

Give a coding agent only the generated workspace and its `TASK.md`. After it edits `app.py`, grade it from this repository:

```sh
python bench.py grade attachment ../attachment-workspace
```

`grade` returns JSON and exits successfully only when every acceptance group passes. The starter is intentionally broken. Use a fresh output directory for each attempt. The grader lives outside the candidate workspace.

## Task catalog

| Task | Engineering problem | Important checks |
| --- | --- | --- |
| [attachment](tasks/attachment/TASK.md) | A cached attachment endpoint fails | Original first, bounded fallback, file size, timeout, failure propagation |
| [routing](tasks/routing/TASK.md) | Two agents compete for a reply | Direct address, reply ownership, channel block, stable cross-process choice |
| [voice](tasks/voice/TASK.md) | Invalid audio looks like valid speech | PCM shape, encrypted-frame rejection, captions, confidence metadata |
| [memory](tasks/memory/TASK.md) | Facts lose their speaker or evidence | User isolation, source validation, confidence paired with evidence, copy safety |
| [pagination](tasks/pagination/TASK.md) | A reading stops midway | Ten sections, three ordered messages, limits, all-or-nothing validation |

Every task has a broken `starter/app.py`, a public smoke test, a complete contract, four acceptance groups, and `reference/app.py`. The reference implementations illustrate one valid solution; the grader tests behavior instead of exact source text.

## Validate the task materials

```sh
python bench.py validate
```

This checks that every reference meets its acceptance contract, every starter fails at least one group, and an invalid submission receives no credit. This is harness validation, not an experiment measuring coding-agent capability. GitHub Actions repeats these checks on Python 3.11 and 3.12.

## Rubric and limitations

Each of four test methods is one acceptance group worth 25 points. A group containing multiple assertions earns credit only when all its assertions pass. The maximum is 100. Import failures, timeouts, and malformed grader output earn zero. Scores are task-local correctness checks, not estimates of intelligence or production readiness.

These are deliberately small, synthetic reproductions. They do not reproduce an entire deployed bot, provider outage, Discord gateway, acoustic environment, or DAVE implementation. In particular, the voice task accepts an already-decoded PCM buffer and an explicit encrypted flag; it does not implement decryption or speech recognition.

All graders and reference solutions are public. Examples beyond the smoke test are public acceptance cases, not secret holdouts. They must not be described as a contamination-resistant benchmark. A separate private set and independent review would be needed for that claim.

Candidate programs execute as Python code. A subprocess timeout is not a security sandbox. Run unfamiliar submissions in a disposable environment without credentials or access to personal files. No network calls are needed by the supplied materials.

## Engineering evidence

- [PDF retrieval incident](docs/pdf-retrieval.md): observed production failure, narrow fix, and verification boundaries.
- [Turn ownership design](docs/turn-ownership.md): a design case study and reproducible specification.
- [Contribution and AI assistance](CONTRIBUTIONS.md): how this portfolio was developed and what it does not claim.
- [Review guide](docs/review-guide.md): a short route through the source and evidence.

The task data is synthetic. No private chat logs, voice recordings, user memory databases, credentials, or uploaded study document are distributed.
