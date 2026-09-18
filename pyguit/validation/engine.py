from __future__ import annotations

import re
from typing import Any

from pyguit.automation.exceptions import ValidationError
from pyguit.ocr.image_match import find_template
from pyguit.ocr.reader import OCRReader
from pyguit.validation.result import ValidationResult
from pyguit.validation.rules import ComparisonOp, ValidationRule, load_rules_from_yaml


class ValidationEngine:
    """Runs validation rules against observed state from OCR or manual input."""

    def __init__(self, ocr_reader: OCRReader | None = None) -> None:
        self._ocr = ocr_reader
        self._rules: list[ValidationRule] = []
        self._results: list[ValidationResult] = []

    @property
    def rules(self) -> list[ValidationRule]:
        return list(self._rules)

    @property
    def results(self) -> list[ValidationResult]:
        return list(self._results)

    def load_rules(self, yaml_path: str) -> None:
        self._rules.extend(load_rules_from_yaml(yaml_path))

    def add_rule(self, rule: ValidationRule) -> None:
        self._rules.append(rule)

    def clear_results(self) -> None:
        self._results.clear()

    def validate_state(
        self, observed_state: dict[str, str]
    ) -> list[ValidationResult]:
        results = []
        for rule in self._rules:
            if rule.operator == ComparisonOp.IMAGE_MATCH:
                continue
            observed = observed_state.get(rule.field, "")
            result = self._evaluate_rule(rule, observed)
            results.append(result)
        self._results.extend(results)
        return results

    def validate_screenshot(
        self,
        screenshot_path: str,
        ocr_reader: OCRReader | None = None,
    ) -> list[ValidationResult]:
        reader = ocr_reader or self._ocr
        results = []

        text_rules = [
            r for r in self._rules if r.operator != ComparisonOp.IMAGE_MATCH
        ]
        image_rules = [
            r for r in self._rules if r.operator == ComparisonOp.IMAGE_MATCH
        ]

        if text_rules and reader:
            state = reader.read_structured(screenshot_path)
            for rule in text_rules:
                observed = state.get(rule.field, "")
                result = self._evaluate_rule(rule, observed)
                result.evidence_path = screenshot_path
                results.append(result)

        for rule in image_rules:
            result = self.validate_image(rule, screenshot_path)
            results.append(result)

        self._results.extend(results)
        return results

    def validate_text(
        self, rule: ValidationRule, observed_text: str
    ) -> ValidationResult:
        result = self._evaluate_rule(rule, observed_text)
        self._results.append(result)
        return result

    def validate_numeric(
        self, rule: ValidationRule, observed_value: float
    ) -> ValidationResult:
        result = self._evaluate_numeric_rule(rule, observed_value)
        self._results.append(result)
        return result

    def validate_image(
        self, rule: ValidationRule, screenshot_path: str
    ) -> ValidationResult:
        match = find_template(screenshot_path, str(rule.expected))
        if match is None:
            result = ValidationResult(
                rule_name=rule.name,
                passed=False,
                expected=rule.expected,
                observed="image not found or could not be loaded",
                message="Template matching failed",
                evidence_path=screenshot_path,
            )
        else:
            _, _, confidence = match
            passed = confidence >= rule.confidence
            result = ValidationResult(
                rule_name=rule.name,
                passed=passed,
                expected=f">= {rule.confidence:.2f} confidence",
                observed=f"{confidence:.4f}",
                message="" if passed else f"Confidence {confidence:.4f} below threshold {rule.confidence}",
                evidence_path=screenshot_path,
            )
        self._results.append(result)
        return result

    def get_summary(self) -> dict[str, Any]:
        passed = sum(1 for r in self._results if r.passed)
        failed = len(self._results) - passed
        return {
            "total": len(self._results),
            "passed": passed,
            "failed": failed,
            "results": [r.to_dict() for r in self._results],
        }

    def assert_all_passed(self) -> None:
        failed = [r for r in self._results if not r.passed]
        if failed:
            messages = [f"  - {r.rule_name}: expected={r.expected}, observed={r.observed}" for r in failed]
            raise ValidationError(
                f"{len(failed)} validation(s) failed:\n" + "\n".join(messages)
            )

    def _evaluate_rule(
        self, rule: ValidationRule, observed: str
    ) -> ValidationResult:
        op = rule.operator
        expected = str(rule.expected)
        passed = False
        message = ""

        if op == ComparisonOp.EQUALS:
            if rule.tolerance and _is_numeric(expected) and _is_numeric(observed):
                return self._evaluate_numeric_rule(rule, float(observed))
            passed = observed.lower() == expected.lower()
            if not passed:
                message = f"Expected '{expected}', got '{observed}'"

        elif op == ComparisonOp.CONTAINS:
            passed = expected.lower() in observed.lower()
            if not passed:
                message = f"'{expected}' not found in '{observed}'"

        elif op == ComparisonOp.NOT_CONTAINS:
            passed = expected.lower() not in observed.lower()
            if not passed:
                message = f"'{expected}' was found in '{observed}'"

        elif op == ComparisonOp.MATCHES:
            passed = bool(re.search(expected, observed))
            if not passed:
                message = f"Pattern '{expected}' did not match '{observed}'"

        elif op in (ComparisonOp.GREATER_THAN, ComparisonOp.LESS_THAN, ComparisonOp.IN_RANGE):
            if _is_numeric(observed):
                return self._evaluate_numeric_rule(rule, float(observed))
            passed = False
            message = f"Cannot compare non-numeric value '{observed}'"

        return ValidationResult(
            rule_name=rule.name,
            passed=passed,
            expected=expected,
            observed=observed,
            message=message,
        )

    def _evaluate_numeric_rule(
        self, rule: ValidationRule, observed_value: float
    ) -> ValidationResult:
        op = rule.operator
        expected = rule.expected
        passed = False
        message = ""

        if op == ComparisonOp.EQUALS:
            target = float(expected)
            passed = abs(observed_value - target) <= rule.tolerance
            if not passed:
                message = f"Expected {target} ± {rule.tolerance}, got {observed_value}"

        elif op == ComparisonOp.GREATER_THAN:
            target = float(expected)
            passed = observed_value > target
            if not passed:
                message = f"Expected > {target}, got {observed_value}"

        elif op == ComparisonOp.LESS_THAN:
            target = float(expected)
            passed = observed_value < target
            if not passed:
                message = f"Expected < {target}, got {observed_value}"

        elif op == ComparisonOp.IN_RANGE:
            if isinstance(expected, (list, tuple)) and len(expected) == 2:
                low, high = float(expected[0]), float(expected[1])
            else:
                low, high = 0.0, float(expected)
            passed = low <= observed_value <= high
            if not passed:
                message = f"Expected [{low}, {high}], got {observed_value}"

        return ValidationResult(
            rule_name=rule.name,
            passed=passed,
            expected=str(expected),
            observed=str(observed_value),
            message=message,
        )


def _is_numeric(value: str) -> bool:
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False
