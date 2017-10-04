from astroid import Const

from django_lint.ast_utils import find_all_model_fields, get_call_kwargs
from django_lint.checks.base import Check
from django_lint.consts import KNOWN_ACRONYMS


class FieldVerboseNameCapitalization(Check):
    id = 'field-verbose-name-capitalization'
    description = """Check that field verbose_names are not capitalized"""

    def check(self):
        for cdef, assign in find_all_model_fields(self.context, self.file_context.ast):
            field_kwargs = get_call_kwargs(assign.value)
            vn_node = field_kwargs.get('verbose_name')
            if vn_node and isinstance(vn_node, Const) and isinstance(vn_node.value, str):
                yield from self._check_verbose_name(assign, vn_node)

    def _check_verbose_name(self, assign, vn_node):
        verbose_name = vn_node.value
        if not verbose_name[0].isupper():
            return
        if any(verbose_name.startswith(acronym) for acronym in KNOWN_ACRONYMS):
            return
        yield self.make_error(
            '`{name}` verbose name `{verbose_name}` should not be capitalized',
            params={
                'name': assign.targets[0],
                'verbose_name': verbose_name,
            },
            node=vn_node,
        )
