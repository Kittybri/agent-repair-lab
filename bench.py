"""Prepare and grade small, offline software-repair tasks."""

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
TASKS = ("attachment", "routing", "voice", "memory", "pagination")


def grade(task, candidate):
    try:
        result = subprocess.run(
            [sys.executable, "-I", str(ROOT / "grading" / "run_task.py"), task, str(candidate.resolve())],
            capture_output=True, text=True, timeout=20,
        )
        report = json.loads(result.stdout)
        if result.returncode or not isinstance(report.get("score"), (int, float)):
            raise ValueError("Grader did not return a valid result")
        return report
    except (subprocess.TimeoutExpired, ValueError, OSError):
        return {"task": task, "score": 0, "error": "Grader failed or exceeded 20 seconds"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    prepare = sub.add_parser("prepare")
    prepare.add_argument("task", choices=TASKS)
    prepare.add_argument("output", type=Path)
    evaluate = sub.add_parser("grade")
    evaluate.add_argument("task", choices=TASKS)
    evaluate.add_argument("workspace", type=Path)
    sub.add_parser("validate")
    args = parser.parse_args()
    if args.command == "prepare":
        if args.output.exists():
            parser.error("Output already exists; choose a fresh workspace")
        shutil.copytree(ROOT / "tasks" / args.task / "starter", args.output)
        shutil.copyfile(ROOT / "tasks" / args.task / "TASK.md", args.output / "TASK.md")
        print(f"Prepared {args.task} in {args.output}")
        return 0
    if args.command == "grade":
        report = grade(args.task, args.workspace / "app.py")
        print(json.dumps(report, indent=2))
        return 0 if report.get("score") == 100 else 1
    valid = True
    for task in TASKS:
        starter = grade(task, ROOT / "tasks" / task / "starter" / "app.py")
        reference = grade(task, ROOT / "tasks" / task / "reference" / "app.py")
        okay = starter.get("score", 100) < 100 and reference.get("score") == 100
        valid &= okay
        print(f"{task}: {'PASS' if okay else 'FAIL'} (starter fails acceptance; reference passes)" if okay else json.dumps({"starter": starter, "reference": reference}))
        with tempfile.TemporaryDirectory() as directory:
            stub = Path(directory) / "app.py"
            stub.write_text("raise RuntimeError('invalid submission')\n", encoding="utf-8")
            if grade(task, stub).get("score") != 0:
                valid = False
                print(f"{task}: FAIL invalid submission received credit")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
