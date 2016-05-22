# -*- coding: utf-8 -*-
from __future__ import absolute_import

import datetime
from unittest import TestCase

from microschema import (
    validate,
    convert,
    ValidationError,
    ConversionError,
)


# TODO: test required field
# TODO: test when inferred value is missing
# TODO: test compound type

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
            'none': {'type': None},
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
            'none': None,
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
            'none': 'foo',
        }
        with self.assertRaises(ValidationError) as cm:
            validate(schema, data)
        message = {
            'str': u'Field must be a str instance, got: int.',
            'unicode': u'Field must be a unicode instance, got: int.',
            'basestring': u'Field must be a basestring instance, got: int.',
            'dict': u'Field must be a dict instance, got: int.',
            'list': u'Field must be a list instance, got: int.',
            'int': u'Field must be a int instance, got: str.',
            'long': u'Field must be a long instance, got: str.',
            'float': u'Field must be a float instance, got: int.',
            'bool': u'Field must be a bool instance, got: str.',
            'none': u'Field must be None, got: str.',
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
            'damage': {
                'validator': self._damage_validator,
            },
        }

        # valid
        data = {'category': 'sword', 'damage': 100}
        self.assertEqual(validate(schema, data), data)

        # invalid
        data = {'category': 'sword', 'damage': 1000}
        with self.assertRaises(ValidationError) as cm:
            validate(schema, data)
        message = {'damage': u'Swords can not have damage greater then 100.'}
        self.assertEqual(cm.exception.message, message)

    def _username_validator(self, name, defs, data, value, context=None):
        if not isinstance(value, str):
            raise ValidationError(u'Field must be a str instance.')

        if not value.islower():
            raise ValidationError(u'Upper case letters not allowed.')

        return value

    def _damage_validator(self, name, defs, data, value, context=None):
        if not isinstance(value, int):
            raise ValidationError(u'Field must be a int instance.')

        if data['category'] == 'sword':
            if value > 100:
                message = u'Swords can not have damage greater then 100.'
                raise ValidationError(message)

        return value


class TestConversion(TestCase):
    def test_with_validation(self):
        # valid
        schema = {'str': {'type': str}}
        data = {'str': 'string'}
        self.assertEqual(convert(schema, data), data)

        # invalid
        schema = {'str': {'type': str}}
        data = {'str': 'string', 'int': 1}
        with self.assertRaises(ValidationError) as cm:
            convert(schema, data)
        message = {'int': u'Rogue field.'}
        self.assertEqual(cm.exception.message, message)

    def test_without_validation(self):
        # valid
        schema = {'str': {'type': str}}
        data = {'str': 'string'}
        self.assertEqual(convert(schema, data, validated=True), data)

        # rogue fields
        schema = {'str': {'type': str}}
        data = {'str': 'string', 'int': 1}
        self.assertNotEqual(convert(schema, data, validated=True), data)

        # missing fields
        schema = {'str': {'type': str}}
        data = {}
        self.assertEqual(convert(schema, data, validated=True), data)

    def test_with_non_required_list(self):
	schema = {
	    'non_required_list': {
	        'type': list,
	        'required': False,
	        'schema': {'field1': {'type': int},
			   'field2': {'type': unicode}
                          }
		}
    	}
	data = {}
	self.assertEqual(convert(schema, data, validated=True), data)
	data = {'non_required_list': []}
        self.assertEqual(convert(schema, data, validated=True), data)
	data = {'non_required_list': [{'field1': 1, 'field2': u'value'}]}
        self.assertEqual(convert(schema, data, validated=True), data)

    def test_custom_converter(self):
        schema = {
            'timestamp': {
                'type': int,
                'required': True,
                'converter': self._timestamp_convertor
            },
        }

        dt = datetime.datetime(2014, 12, 13, 21, 45, 28)
        ts = int(dt.strftime('%s'))

        data = {'timestamp': ts}
        converted_data = {'timestamp': dt}

        ttt = convert(schema, data)
        self.assertEqual(ttt, converted_data)

    def test_conversion_exception(self):
        schema = {
            'timestamp': {
                'type': int,
                'required': True,
                'converter': self._timestamp_convertor
            },
        }

        data = {'timestamp': 1000000000000}
        with self.assertRaises(ConversionError) as cm:
            convert(schema, data)
        message = {'timestamp': u'year is out of range'}
        self.assertEqual(cm.exception.message, message)

    def _timestamp_convertor(self, defs, data, value):
        try:
            return datetime.datetime.fromtimestamp(value)
        except ValueError as e:
            raise ConversionError(unicode(e.message))
