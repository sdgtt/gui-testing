from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


@dataclass
class TestMetadata:
    """Stores metadata for a single test run's evidence."""

    test_name: str
    device: str = ""
    status: str = "unknown"
    start_time: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    end_time: str = ""
    screenshots: list[str] = field(default_factory=list)
    logs: list[str] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)
    extra: dict = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_json(cls, data: str) -> TestMetadata:
        return cls(**json.loads(data))

    @classmethod
    def from_file(cls, path: str) -> TestMetadata:
        with open(path) as f:
            return cls(**json.load(f))
