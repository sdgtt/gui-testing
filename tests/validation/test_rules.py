import os
import tempfile

import yaml

from pyguit.validation.rules import ComparisonOp, ValidationRule, load_rules_from_yaml


class TestComparisonOp:
    def test_all_values(self):
        expected = {
            "equals", "contains", "not_contains", "matches",
            "greater_than", "less_than", "in_range", "image_match",
        }
        assert {op.value for op in ComparisonOp} == expected


class TestValidationRule:
    def test_defaults(self):
        rule = ValidationRule(
            name="test", field="status", operator=ComparisonOp.EQUALS, expected="ok"
        )
        assert rule.tolerance == 0.0
        assert rule.confidence == 0.9
        assert rule.description == ""


class TestLoadRulesFromYaml:
    def test_load_expected_section(self):
        data = {
            "expected": {
                "device": "connected",
                "streaming": "active",
            }
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(data, f)
            path = f.name
        try:
            rules = load_rules_from_yaml(path)
            assert len(rules) == 2
            names = {r.name for r in rules}
            assert "check_device" in names
            assert "check_streaming" in names
            for r in rules:
                assert r.operator == ComparisonOp.EQUALS
        finally:
            os.unlink(path)

    def test_load_validations_section(self):
        data = {
            "validations": [
                {
                    "name": "check_temp",
                    "field": "temperature",
                    "operator": "greater_than",
                    "expected": 20,
                    "tolerance": 0.5,
                    "description": "Temperature must be above 20",
                }
            ]
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(data, f)
            path = f.name
        try:
            rules = load_rules_from_yaml(path)
            assert len(rules) == 1
            assert rules[0].name == "check_temp"
            assert rules[0].operator == ComparisonOp.GREATER_THAN
            assert rules[0].tolerance == 0.5
        finally:
            os.unlink(path)
