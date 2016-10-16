.. image:: https://travis-ci.org/amibiz/microschema.svg?branch=develop
    :target: https://travis-ci.org/amibiz/microschema


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

