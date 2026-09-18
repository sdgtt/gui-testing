from pyguit.evidence.metadata import TestMetadata


class TestTestMetadata:
    def test_round_trip_json(self):
        meta = TestMetadata(test_name="test_foo", device="ADALM2000", status="pass")
        json_str = meta.to_json()
        restored = TestMetadata.from_json(json_str)
        assert restored.test_name == "test_foo"
        assert restored.device == "ADALM2000"
        assert restored.status == "pass"

    def test_default_values(self):
        meta = TestMetadata(test_name="t")
        assert meta.device == ""
        assert meta.status == "unknown"
        assert meta.start_time
        assert meta.screenshots == []
        assert meta.logs == []
        assert meta.artifacts == []

    def test_to_dict(self):
        meta = TestMetadata(test_name="t", device="d")
        d = meta.to_dict()
        assert isinstance(d, dict)
        assert d["test_name"] == "t"
        assert d["device"] == "d"
