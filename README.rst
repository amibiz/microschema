.. image:: https://travis-ci.org/amibiz/microschema.svg?branch=develop
    :target: https://travis-ci.org/amibiz/microschema

.. image:: https://coveralls.io/repos/github/amibiz/microschema/badge.svg
    :target: https://coveralls.io/github/amibiz/microschema

MicroSchema
-----------

Example:

    >>> import microschema
    >>> schema = {
    ...     'username': {'type': str, 'required': True},
    ...     'score': {'type': int},
    ... }
    >>> data = {
    ...     'username': 'foobar',
    ...     'score': 10000,
    ... }
    >>> print microschema.validate(schema, data)


Python Compatibility
--------------------

Currently, only python 2.7 is supported.
