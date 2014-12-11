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

