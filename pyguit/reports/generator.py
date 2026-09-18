from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

from jinja2 import Environment, FileSystemLoader

from pyguit.evidence.metadata import TestMetadata
from pyguit.validation.result import ValidationResult

_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


class ReportGenerator:
    """Generates Markdown validation reports from validation results and evidence."""

    def __init__(self, template_dir: str | None = None) -> None:
        self._env = Environment(
            loader=FileSystemLoader(template_dir or _TEMPLATE_DIR),
            keep_trailing_newline=True,
        )

    def generate(
        self,
        results: list[ValidationResult],
        metadata: TestMetadata,
        output_path: str,
    ) -> str:
        passed_count = sum(1 for r in results if r.passed)
        failed_count = len(results) - passed_count
        all_passed = failed_count == 0

        duration = ""
        if metadata.end_time and metadata.start_time:
            try:
                start = datetime.fromisoformat(metadata.start_time)
                end = datetime.fromisoformat(metadata.end_time)
                delta = end - start
                duration = f"{delta.total_seconds():.1f}s"
            except (ValueError, TypeError):
                pass

        template = self._env.get_template("report.md.j2")
        content = template.render(
            metadata=metadata,
            results=results,
            all_passed=all_passed,
            passed_count=passed_count,
            failed_count=failed_count,
            duration=duration,
        )

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w") as f:
            f.write(content)
        return output_path

    def generate_summary(
        self,
        all_runs: list[dict[str, Any]],
        output_path: str,
    ) -> str:
        """Generate a suite summary report.

        all_runs: list of dicts with keys:
            test_name, results (list[ValidationResult])
        """
        runs = []
        failed_runs = []
        total_passed = 0
        total_failed = 0

        for run_data in all_runs:
            test_name = run_data["test_name"]
            results = run_data["results"]
            passed = sum(1 for r in results if r.passed)
            failed = len(results) - passed
            all_passed = failed == 0

            run_info = {
                "test_name": test_name,
                "all_passed": all_passed,
                "total": len(results),
                "passed": passed,
                "failed": failed,
                "failed_results": [r for r in results if not r.passed],
            }
            runs.append(run_info)
            if not all_passed:
                failed_runs.append(run_info)
                total_failed += 1
            else:
                total_passed += 1

        template = self._env.get_template("summary.md.j2")
        content = template.render(
            timestamp=datetime.now(timezone.utc).isoformat(),
            total_tests=len(runs),
            passed_tests=total_passed,
            failed_tests=total_failed,
            runs=runs,
            failed_runs=failed_runs,
        )

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w") as f:
            f.write(content)
        return output_path
