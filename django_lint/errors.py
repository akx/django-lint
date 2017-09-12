from astroid.node_classes import NodeNG


def _massage_parameters_for_format(p):
    params = {}
    for key, value in p.items():
        if isinstance(value, NodeNG):
            value = value._repr_name()
        else:
            value = str(value)
        params[key] = value
    return params


class Error(object):
    def __init__(self, *, check, code, file_context, message, params=None, node=None):
        """
        :type check: django_lint.checks.base.Check
        :type code: str
        :type file_context: django_lint.contexts.FileContext
        :type message: str
        :type params: dict[str, object]
        :type node: astroid.node_classes.NodeNG
        """
        self.check = check
        self.file_context = file_context
        self.message = str(message)
        self.params = (params or {})
        self.code = code
        self.node = node

    @property
    def formatted_message(self):
        return self.message.format_map(_massage_parameters_for_format(self.params))

    @property
    def full_code(self):
        code = self.check.id
        if self.code:
            code += ':%s' % self.code
        return code

    @property
    def location(self):
        location = self.file_context.relative_path
        if self.node:
            location += ':%s' % self.node.lineno
        return location

    def __str__(self):
        return '{location} - {full_code}: {message}'.format(
            location=self.location,
            full_code=self.full_code,
            message=self.formatted_message,
        )
