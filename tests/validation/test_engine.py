import pytest

from pyguit.automation.exceptions import ValidationError
from pyguit.validation.engine import ValidationEngine
from pyguit.validation.rules import ComparisonOp, ValidationRule


class TestValidationEngine:
    def _make_engine(self, *rules):
        engine = ValidationEngine()
        for r in rules:
            engine.add_rule(r)
        return engine

    def test_equals_pass(self):
        engine = self._make_engine(
            ValidationRule("r1", "status", ComparisonOp.EQUALS, "active")
        )
        results = engine.validate_state({"status": "active"})
        assert len(results) == 1
        assert results[0].passed

    def test_equals_fail(self):
        engine = self._make_engine(
            ValidationRule("r1", "status", ComparisonOp.EQUALS, "active")
        )
        results = engine.validate_state({"status": "inactive"})
        assert len(results) == 1
        assert not results[0].passed

    def test_equals_case_insensitive(self):
        engine = self._make_engine(
            ValidationRule("r1", "status", ComparisonOp.EQUALS, "Active")
        )
        results = engine.validate_state({"status": "active"})
        assert results[0].passed

    def test_contains_pass(self):
        engine = self._make_engine(
            ValidationRule("r1", "log", ComparisonOp.CONTAINS, "success")
        )
        results = engine.validate_state({"log": "Operation success completed"})
        assert results[0].passed

    def test_not_contains_pass(self):
        engine = self._make_engine(
            ValidationRule("r1", "log", ComparisonOp.NOT_CONTAINS, "error")
        )
        results = engine.validate_state({"log": "All good"})
        assert results[0].passed

    def test_not_contains_fail(self):
        engine = self._make_engine(
            ValidationRule("r1", "log", ComparisonOp.NOT_CONTAINS, "error")
        )
        results = engine.validate_state({"log": "Fatal error occurred"})
        assert not results[0].passed

    def test_matches_regex(self):
        engine = self._make_engine(
            ValidationRule("r1", "version", ComparisonOp.MATCHES, r"\d+\.\d+\.\d+")
        )
        results = engine.validate_state({"version": "1.2.3"})
        assert results[0].passed

    def test_numeric_equals_with_tolerance(self):
        rule = ValidationRule(
            "r1", "temp", ComparisonOp.EQUALS, "25.0", tolerance=0.5
        )
        engine = self._make_engine(rule)
        results = engine.validate_state({"temp": "25.3"})
        assert results[0].passed

    def test_numeric_equals_outside_tolerance(self):
        rule = ValidationRule(
            "r1", "temp", ComparisonOp.EQUALS, "25.0", tolerance=0.1
        )
        engine = self._make_engine(rule)
        results = engine.validate_state({"temp": "25.5"})
        assert not results[0].passed

    def test_greater_than(self):
        engine = self._make_engine(
            ValidationRule("r1", "count", ComparisonOp.GREATER_THAN, "10")
        )
        results = engine.validate_state({"count": "15"})
        assert results[0].passed

    def test_less_than(self):
        engine = self._make_engine(
            ValidationRule("r1", "count", ComparisonOp.LESS_THAN, "100")
        )
        results = engine.validate_state({"count": "50"})
        assert results[0].passed

    def test_missing_field_fails(self):
        engine = self._make_engine(
            ValidationRule("r1", "missing", ComparisonOp.EQUALS, "value")
        )
        results = engine.validate_state({})
        assert not results[0].passed

    def test_get_summary(self):
        engine = self._make_engine(
            ValidationRule("r1", "a", ComparisonOp.EQUALS, "x"),
            ValidationRule("r2", "b", ComparisonOp.EQUALS, "y"),
        )
        engine.validate_state({"a": "x", "b": "z"})
        summary = engine.get_summary()
        assert summary["total"] == 2
        assert summary["passed"] == 1
        assert summary["failed"] == 1

    def test_assert_all_passed_raises(self):
        engine = self._make_engine(
            ValidationRule("r1", "a", ComparisonOp.EQUALS, "x"),
        )
        engine.validate_state({"a": "wrong"})
        with pytest.raises(ValidationError):
            engine.assert_all_passed()

    def test_assert_all_passed_ok(self):
        engine = self._make_engine(
            ValidationRule("r1", "a", ComparisonOp.EQUALS, "x"),
        )
        engine.validate_state({"a": "x"})
        engine.assert_all_passed()

    def test_clear_results(self):
        engine = self._make_engine(
            ValidationRule("r1", "a", ComparisonOp.EQUALS, "x"),
        )
        engine.validate_state({"a": "x"})
        assert len(engine.results) == 1
        engine.clear_results()
        assert len(engine.results) == 0
