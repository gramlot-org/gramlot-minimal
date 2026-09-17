import unittest
from gramlot_standalone.envelope import DataEnvelope, EnvelopeError

class EnvelopeTests(unittest.TestCase):
    def test_round_trip_detaches_opaque_json_payload(self):
        payload = {"typed": [0, False, None, "é", {"value": 1.25}]}
        original = DataEnvelope("site", 2, "tytx-json", 1, payload)
        payload["typed"].append("later")
        self.assertNotIn("later", original.application_data["typed"])
        decoded = DataEnvelope.loads(original.dumps(), expected_site_id="site",
                                     expected_schema_version=2)
        self.assertEqual(decoded, original)

    def test_rejects_ui_state_foreign_site_bool_version_and_duplicates(self):
        value = DataEnvelope("site", 1, "codec", 1, None).as_dict()
        value["ui_state"] = {}
        with self.assertRaisesRegex(EnvelopeError, "fields"):
            DataEnvelope.from_mapping(value)
        value.pop("ui_state")
        with self.assertRaisesRegex(EnvelopeError, "different site"):
            DataEnvelope.from_mapping(value, expected_site_id="other")
        value = DataEnvelope("site", 1, "codec", 1, None).as_dict()
        value["version"] = True
        with self.assertRaisesRegex(EnvelopeError, "format or version"):
            DataEnvelope.from_mapping(value)
        with self.assertRaisesRegex(EnvelopeError, "duplicate"):
            DataEnvelope.loads('{"format":"x","format":"y"}')
        valid = DataEnvelope("site", 1, "codec", 1, None).dumps()
        with self.assertRaisesRegex(EnvelopeError, "different typed Bag codec"):
            DataEnvelope.loads(valid, expected_codec="other")
        deep = '{"format":"gramlot-standalone-application-data","version":1,"site_id":"site","schema_version":1,"codec":{"name":"codec","version":1},"application_data":' + "[" * 300 + "null" + "]" * 300 + "}"
        with self.assertRaisesRegex(EnvelopeError, "nesting depth"):
            DataEnvelope.loads(deep)

    def test_rejects_nonfinite_non_json_and_cycles(self):
        with self.assertRaisesRegex(EnvelopeError, "non-finite"):
            DataEnvelope("site", 1, "codec", 1, {"bad": float("nan")})
        with self.assertRaisesRegex(EnvelopeError, "non-JSON"):
            DataEnvelope("site", 1, "codec", 1, {"bad": object()})
        cyclic = []; cyclic.append(cyclic)
        with self.assertRaisesRegex(EnvelopeError, "cyclic"):
            DataEnvelope("site", 1, "codec", 1, cyclic)

if __name__ == "__main__": unittest.main()
