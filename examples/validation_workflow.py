"""Validation workflow example - OCR a screenshot, validate state, generate report."""

from pyguit import (
    EvidenceCollector,
    OCRReader,
    ReportGenerator,
    TestMetadata,
    ValidationEngine,
)

# 1. Set up evidence collection
evidence = EvidenceCollector(
    base_dir="results",
    test_name="streaming_validation",
    device="ADALM2000",
)

# 2. Initialize OCR reader
ocr = OCRReader()

# 3. Read text from a screenshot
screenshot_path = "results/streaming_validation/screenshots/app_state.png"
text = ocr.read_text(screenshot_path)
print(f"OCR text:\n{text}\n")

# 4. Extract structured data
state = ocr.read_structured(screenshot_path)
print(f"Structured state: {state}\n")

# 5. Set up validation engine with rules from YAML
engine = ValidationEngine(ocr_reader=ocr)
engine.load_rules("examples/sample_workflow.yaml")

# 6. Validate the observed state
results = engine.validate_state(state)

# 7. Check results
summary = engine.get_summary()
print(f"Validation: {summary['passed']}/{summary['total']} passed")

# 8. Set evidence status
status = "pass" if summary["failed"] == 0 else "fail"
evidence.set_status(status)
evidence.save_log("validation", str(summary))
meta_path = evidence.finalize()

# 9. Generate markdown report
reporter = ReportGenerator()
reporter.generate(
    results=results,
    metadata=evidence.metadata,
    output_path="results/streaming_validation/report.md",
)
print("Report generated: results/streaming_validation/report.md")
