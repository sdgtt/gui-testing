from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import yaml


class ComparisonOp(Enum):
    EQUALS = "equals"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    MATCHES = "matches"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    IN_RANGE = "in_range"
    IMAGE_MATCH = "image_match"


@dataclass
class ValidationRule:
    name: str
    field: str
    operator: ComparisonOp
    expected: Any
    tolerance: float = 0.0
    confidence: float = 0.9
    description: str = ""


def load_rules_from_yaml(yaml_path: str) -> list[ValidationRule]:
    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    rules: list[ValidationRule] = []

    if "expected" in data:
        for field_name, expected_value in data["expected"].items():
            rules.append(
                ValidationRule(
                    name=f"check_{field_name}",
                    field=field_name,
                    operator=ComparisonOp.EQUALS,
                    expected=str(expected_value),
                )
            )

    if "validations" in data:
        for item in data["validations"]:
            rules.append(
                ValidationRule(
                    name=item["name"],
                    field=item["field"],
                    operator=ComparisonOp(item["operator"]),
                    expected=item["expected"],
                    tolerance=item.get("tolerance", 0.0),
                    confidence=item.get("confidence", 0.9),
                    description=item.get("description", ""),
                )
            )

    return rules
