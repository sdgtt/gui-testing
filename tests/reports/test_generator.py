import os
import tempfile

from pyguit.evidence.metadata import TestMetadata
from pyguit.reports.generator import ReportGenerator
from pyguit.validation.result import ValidationResult


class TestReportGenerator:
    def _make_results(self, pass_count=2, fail_count=1):
        results = []
        for i in range(pass_count):
            results.append(
                ValidationResult(
                    rule_name=f"pass_rule_{i}",
                    passed=True,
                    expected="ok",
                    observed="ok",
                )
            )
        for i in range(fail_count):
            results.append(
                ValidationResult(
                    rule_name=f"fail_rule_{i}",
                    passed=False,
                    expected="ok",
                    observed="bad",
                    message="Mismatch",
                )
            )
        return results

    def test_generate_report(self):
        gen = ReportGenerator()
        results = self._make_results(2, 1)
        meta = TestMetadata(test_name="test_streaming", device="M2K", status="fail")

        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "report.md")
            gen.generate(results, meta, out)
            assert os.path.isfile(out)
            content = open(out).read()
            assert "test_streaming" in content
            assert "FAILED" in content
            assert "pass_rule_0" in content
            assert "fail_rule_0" in content

    def test_generate_all_passed(self):
        gen = ReportGenerator()
        results = self._make_results(3, 0)
        meta = TestMetadata(test_name="test_ok", status="pass")

        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "report.md")
            gen.generate(results, meta, out)
            content = open(out).read()
            assert "PASSED" in content

    def test_generate_summary(self):
        gen = ReportGenerator()
        runs = [
            {
                "test_name": "test_a",
                "results": self._make_results(2, 0),
            },
            {
                "test_name": "test_b",
                "results": self._make_results(1, 1),
            },
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "summary.md")
            gen.generate_summary(runs, out)
            assert os.path.isfile(out)
            content = open(out).read()
            assert "test_a" in content
            assert "test_b" in content
            assert "Total Tests" in content
