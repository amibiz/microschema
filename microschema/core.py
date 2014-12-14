# -*- coding: utf-8 -*-
from __future__ import absolute_import


class ValidationError(ValueError):
    pass

class ConversionError(ValueError):
    pass


messages = {
    'input': u'input {name} must be a dictionary instance, got: {type}.',
    'rogue': u'Rogue field.',
    'missing': u'Missing required field.',
    'field': u'Field must be a {schema_type} instance, got: {field_type}.',
    'schema': u'Missing schema definition.',
}


def validate(schema, data):
    """Validates data based on a given schema."""

    if not isinstance(schema, dict):
        instance_type = type(schema).__name__
        message = messages['input']
        raise TypeError(message.format(name='schema', type=instance_type))

    if not isinstance(data, dict):
        instance_type = type(data).__name__
        message = messages['input']
        raise TypeError(message.format(name='data', type=instance_type))

    errors = {}
    schema_fields = set(schema.keys())
    data_fields = set(data.keys())

    # find rogue fields
    rogue_fields = data_fields - schema_fields
    for field in rogue_fields:
        errors.update({field: messages['rogue']})

    # validate each field in the schema
    for name, defs in schema.iteritems():
        field = data.get(name)
        required = defs.get('required', False)

        # report missing required fields
        if required and data.get(name) is None:
            errors.update({name: messages['missing']})
            continue

        # skip missing fields
        if data.get(name) is None:
            continue

        # validate field
        validator = defs.get('validator', default_validator)
        try:
            validator(name, defs, data, field)
        except ValidationError as e:
            errors.update({name: e.message})

    if errors:
        raise ValidationError(errors)

    return data


def convert(schema, data, validated=False):
    """Convert data based on a given schema."""

    if not validated:
        validate(schema, data)

    errors = {}
    converted_data = {}

    # convert each field in the schema
    for name, defs in schema.iteritems():
        field = data.get(name)

        # convert field
        convertor = defs.get('convertor', default_convertor)
        try:
            converted_data[name] = convertor(defs, data, field)
        except ConversionError as e:
            errors.update({name: e.message})

    if errors:
        raise ConversionError(errors)

    return converted_data


def default_validator(name, defs, data, value):
    schema_type = defs['type']
    compound_type = defs.get('compound_type')

    if not isinstance(value, schema_type):
        message = messages['field'].format(
            schema_type=schema_type.__name__,
            field_type=type(value).__name__,
        )
        raise ValidationError(message)

    if schema_type == dict:
        validate(defs['schema'], value)

    errors = {}
    if schema_type == list:
        for index, item in enumerate(value):
            try:
                if compound_type is not None:
                    schema = {'type': compound_type}
                else:
                    schema = defs['schema']
                default_validator(index, schema, value, item)
            except KeyError as e:
                print e
                errors.update({index: messages['schema']})
            except (TypeError, ValidationError) as e:
                errors.update({index: e.message})

    if errors:
        raise ValidationError(errors)

    return value


def default_convertor(defs, data, value):
    compound_type = defs.get('compound_type')
    if compound_type is not None:
        schema_type = compound_type
    else:
        schema_type = defs['type']

    if schema_type == dict:
        return convert(defs['schema'], value)

    errors = {}
    converted_data = []
    if schema_type == list:
        for index, item in enumerate(value):
            try:
                converted_data.append(convert(defs['schema'], item))
            except ConversionError as e:
                errors.update({index: e.message})
        return converted_data

    if errors:
        raise ConversionError(errors)

    return value
