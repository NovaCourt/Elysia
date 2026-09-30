# Falsifier for contract/request_npc_depth.schema.json -- written before the schema exists, so it stands failing
# until the schema lands. Brings its own world: only the schema file and the payloads below.
# Run from the repository root: .venv/bin/python -m unittest discover -s tests
import json
import pathlib
import unittest

import jsonschema
from jsonschema import Draft202012Validator

SCHEMA_PATH = pathlib.Path(__file__).resolve().parent.parent / 'contract' / 'request_npc_depth.schema.json'


def load():
    return json.loads(SCHEMA_PATH.read_text(encoding='utf-8'))


def validator(part):
    schema = load()
    # validate against one of the two named parts, keeping $defs resolvable
    sub = {'$schema': schema.get('$schema'), '$defs': schema['$defs'], '$ref': '#/$defs/' + part}
    return Draft202012Validator(sub)


GOOD_REQUEST = {'contract_version': 1, 'npc_id': 'party-3', 'context_summary': 'The player thanked her for the rescue.'}
DEPTH_REPLY = {'contract_version': 1, 'refused': False, 'text': 'She smiles and says it was nothing.'}
REFUSAL = {'contract_version': 1, 'refused': True, 'reason': 'distress', 'fallback': 'plain_python'}


class TestRequestNpcDepthSchema(unittest.TestCase):
    def test_01_file_parses_as_json(self):
        self.assertIsInstance(load(), dict)

    def test_02_is_a_valid_2020_12_schema(self):
        schema = load()
        self.assertEqual(schema.get('$schema'), 'https://json-schema.org/draft/2020-12/schema')
        Draft202012Validator.check_schema(schema)

    def test_03_carries_integer_version_1(self):
        self.assertIs(type(load().get('version')), int)
        self.assertEqual(load()['version'], 1)

    def test_04_names_request_and_reply(self):
        self.assertIn('request', load()['$defs'])
        self.assertIn('reply', load()['$defs'])

    def test_05_good_request_passes(self):
        validator('request').validate(GOOD_REQUEST)

    def test_06_request_without_npc_id_fails(self):
        bad = dict(GOOD_REQUEST); del bad['npc_id']
        self.assertFalse(validator('request').is_valid(bad))

    def test_07_request_with_unknown_field_fails(self):
        self.assertFalse(validator('request').is_valid(dict(GOOD_REQUEST, surprise=1)))

    def test_08_any_distress_field_is_optional_and_advisory(self):
        req = load()['$defs']['request']
        names = [n for n in req.get('properties', {}) if 'distress' in n]
        for n in names:
            self.assertNotIn(n, req.get('required', []), n + ' must never be required')
            desc = req['properties'][n].get('description', '').lower()
            self.assertTrue('advisory' in desc or 'hint' in desc, n + ' must say it is advisory: the Court decides')

    def test_09_depth_reply_passes(self):
        validator('reply').validate(DEPTH_REPLY)

    def test_10_distress_refusal_passes(self):
        validator('reply').validate(REFUSAL)

    def test_11_refusal_without_reason_fails(self):
        bad = dict(REFUSAL); del bad['reason']
        self.assertFalse(validator('reply').is_valid(bad))

    def test_12_refusal_with_unknown_reason_fails(self):
        self.assertFalse(validator('reply').is_valid(dict(REFUSAL, reason='banana')))

    def test_13_refusal_carrying_text_fails(self):
        self.assertFalse(validator('reply').is_valid(dict(REFUSAL, text='she speaks anyway')))

    def test_14_refusal_fallback_is_plain_python(self):
        self.assertFalse(validator('reply').is_valid(dict(REFUSAL, fallback='something_else')))

    def test_15_empty_reply_fails(self):
        self.assertFalse(validator('reply').is_valid({}))


if __name__ == '__main__':
    unittest.main()
