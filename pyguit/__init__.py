"""PyGUIt - AI-assisted GUI validation platform for hardware testing."""

__version__ = "2.0.0"

from pyguit.automation.controller import GUIController
from pyguit.automation.exceptions import (
    PyGUItError,
    ValidationError,
    WindowNotFoundError,
)
from pyguit.evidence.collector import EvidenceCollector
from pyguit.evidence.metadata import TestMetadata
from pyguit.ocr.reader import OCRReader
from pyguit.reports.generator import ReportGenerator
from pyguit.validation.engine import ValidationEngine

__all__ = [
    "GUIController",
    "EvidenceCollector",
    "OCRReader",
    "ReportGenerator",
    "TestMetadata",
    "ValidationEngine",
    "ValidationError",
    "PyGUItError",
    "WindowNotFoundError",
]
