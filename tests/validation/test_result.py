import json

from pyguit.validation.result import ValidationResult


class TestValidationResult:
    def test_to_dict(self):
        r = ValidationResult(
            rule_name="test",
            passed=True,
            expected="active",
            observed="active",
        )
        d = r.to_dict()
        assert d["rule_name"] == "test"
        assert d["passed"] is True
        assert d["expected"] == "active"
        assert d["observed"] == "active"

    def test_to_json(self):
        r = ValidationResult(
            rule_name="test",
            passed=False,
            expected="x",
            observed="y",
            message="mismatch",
        )
        data = json.loads(r.to_json())
        assert data["passed"] is False
        assert data["message"] == "mismatch"

    def test_timestamp_auto_set(self):
        r = ValidationResult(rule_name="t", passed=True, expected="a", observed="a")
        assert r.timestamp
