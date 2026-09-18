"""Evidence subpackage - screenshot, log, and artifact collection."""

from pyguit.evidence.collector import EvidenceCollector
from pyguit.evidence.metadata import TestMetadata

__all__ = ["EvidenceCollector", "TestMetadata"]
