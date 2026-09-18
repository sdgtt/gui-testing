import json
import os
import tempfile

from pyguit.evidence.collector import EvidenceCollector


class TestEvidenceCollector:
    def test_creates_directory_structure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            collector = EvidenceCollector(
                base_dir=tmpdir, test_name="test_foo"
            )
            assert os.path.isdir(os.path.join(tmpdir, "test_foo", "screenshots"))
            assert os.path.isdir(os.path.join(tmpdir, "test_foo", "logs"))
            assert os.path.isdir(os.path.join(tmpdir, "test_foo", "artifacts"))

    def test_save_log(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            collector = EvidenceCollector(base_dir=tmpdir, test_name="t")
            path = collector.save_log("app", "some log content")
            assert os.path.isfile(path)
            with open(path) as f:
                assert f.read() == "some log content"
            assert path in collector.metadata.logs

    def test_save_artifact(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            collector = EvidenceCollector(base_dir=tmpdir, test_name="t")
            path = collector.save_artifact("data.bin", b"\x00\x01\x02")
            assert os.path.isfile(path)
            with open(path, "rb") as f:
                assert f.read() == b"\x00\x01\x02"

    def test_finalize_writes_metadata(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            collector = EvidenceCollector(
                base_dir=tmpdir, test_name="t", device="M2K"
            )
            collector.set_status("pass")
            meta_path = collector.finalize()
            assert os.path.isfile(meta_path)
            with open(meta_path) as f:
                data = json.load(f)
            assert data["test_name"] == "t"
            assert data["device"] == "M2K"
            assert data["status"] == "pass"
            assert data["end_time"]
