# -*- coding: utf-8 -*-
from __future__ import absolute_import

from unittest import TestCase

from microschema import validate, ValidationError


# TODO: test required field
# TODO: test when inferred value is missing

class TestValidation(TestCase):
    def test_empty(self):
        schema = {}
        data = {}
        self.assertEqual(validate(schema, data), data)

    def test_rogue_field(self):
        # empty schema
        schema = {}
        data = {'str': 'foo'}
        with self.assertRaises(ValidationError) as cm:
            validate(schema, data)
        message = {'str': u'Rogue field.'}
        self.assertEqual(cm.exception.message, message)

        # non-empty schema
        schema = {'str': {'type': str}}
        data = {'str': 'string', 'int': 1}
        with self.assertRaises(ValidationError) as cm:
            validate(schema, data)
        message = {'int': u'Rogue field.'}
        self.assertEqual(cm.exception.message, message)

        # multi rogue fields
        schema = {}
        data = {'str': 'foo', 'int': 1}
        with self.assertRaises(ValidationError) as cm:
            validate(schema, data)
        message = {
            'str': u'Rogue field.',
            'int': u'Rogue field.',
        }
        self.assertEqual(cm.exception.message, message)

    def test_built_in_types(self):
        # schema definition
        schema = {
            'str': {'type': str},
            'unicode': {'type': unicode},
            'basestring': {'type': basestring},
            'dict': {'type': dict, 'schema': {}},
            'list': {'type': list},
            'int': {'type': int},
            'long': {'type': long},
            'float': {'type': float},
            'bool': {'type': bool},
        }

        # valid
        data = {
            'str': 'foo',
            'unicode': u'foo',
            'basestring': u'foo',
            'dict': {},
            'list': [],
            'int': 1,
            'long': 10000000000000000000,
            'float': 1.0,
            'bool': True,
        }
        self.assertEqual(validate(schema, data), data)

        # invalid
        data = {
            'str': 1,
            'unicode': 1,
            'basestring': 1,
            'dict': 1,
            'list': 1,
            'int': 'foo',
            'long': 'foo',
            'float': 1,
            'bool': 'foo',
        }
        with self.assertRaises(ValidationError) as cm:
            validate(schema, data)
        message = {
            'str': u'Field must be a str instance.',
            'unicode': u'Field must be a unicode instance.',
            'basestring': u'Field must be a basestring instance.',
            'dict': u'Field must be a dict instance.',
            'list': u'Field must be a list instance.',
            'int': u'Field must be a int instance.',
            'long': u'Field must be a long instance.',
            'float': u'Field must be a float instance.',
            'bool': u'Field must be a bool instance.',
        }
        self.assertEqual(cm.exception.message, message)


class TestCustomValidator(TestCase):
    def test_required(self):
        schema = {
            'username': {
                'required': True,
                'validator': self._username_validator
            },
        }
        data = {}
        with self.assertRaises(ValidationError) as cm:
            validate(schema, data)
        message = {'username': u'Missing required field.'}
        self.assertEqual(cm.exception.message, message)

    def test_valide(self):
        schema = {
            'username': {
                'validator': self._username_validator
            },
        }
        data = {'username': 'foobar'}
        self.assertEqual(validate(schema, data), data)

    def test_invalid(self):
        schema = {
            'username': {
                'validator': self._username_validator
            },
        }

        # non string username
        data = {'username': 1}
        with self.assertRaises(ValidationError) as cm:
            validate(schema, data)
        message = {'username': u'Field must be a str instance.'}
        self.assertEqual(cm.exception.message, message)

        # not lower case
        data = {'username': 'Foobar'}
        with self.assertRaises(ValidationError) as cm:
            validate(schema, data)
        message = {'username': u'Upper case letters not allowed.'}
        self.assertEqual(cm.exception.message, message)

    def test_inferred(self):
        # schema definition
        schema = {
            'category': {
                'type': str,
            },
            'demage': {
                'validator': self._demage_validator,
            },
        }

        # valid
        data = {'category': 'sword', 'demage': 100}
        self.assertEqual(validate(schema, data), data)

        # invalid
        data = {'category': 'sword', 'demage': 1000}
        with self.assertRaises(ValidationError) as cm:
            validate(schema, data)
        message = {'demage': u'Swords can not have demage greater then 100.'}
        self.assertEqual(cm.exception.message, message)

    def _username_validator(self, name, defs, data, value):
        if not isinstance(value, str):
            raise ValidationError(u'Field must be a str instance.')

        if not value.islower():
            raise ValidationError(u'Upper case letters not allowed.')

        return value

    def _demage_validator(self, name, defs, data, value):
        if not isinstance(value, int):
            raise ValidationError(u'Field must be a int instance.')

        if data['category'] == 'sword':
            if value > 100:
                message = u'Swords can not have demage greater then 100.'
                raise ValidationError(message)

        return value
