"""Evaluator entry point. Candidate code executes in this subprocess."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import unittest


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


task, path = sys.argv[1:]
try:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        load("candidate", Path(path))
        checks = load("acceptance", Path(__file__).with_name(f"test_{task}.py"))
        suite = unittest.defaultTestLoader.loadTestsFromModule(checks)
        result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
    failures = len(result.failures) + len(result.errors) + len(result.skipped)
    passed = result.testsRun - failures
    report = {
        "task": task, "checks": result.testsRun, "passed": passed,
        "score": round(100 * passed / result.testsRun, 2) if result.testsRun else 0,
        "failed_checks": [test.id().split(".")[-1] for test, _ in result.failures + result.errors],
    }
except BaseException as error:
    report = {"task": task, "score": 0, "error": type(error).__name__}
print(json.dumps(report))
