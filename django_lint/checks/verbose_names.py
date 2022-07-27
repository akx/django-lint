from astroid import Const

from django_lint.ast_utils import (
    find_all_model_definitions,
    find_all_model_fields,
    get_call_kwargs,
    get_model_meta_assignments,
)
from django_lint.checks.base import Check
from django_lint.consts import KNOWN_ACRONYMS


class BaseVerboseNameCapitalizationCheck(Check):
    def _check_verbose_name(self, context_name, vn_node):
        if not (
            vn_node and isinstance(vn_node, Const) and isinstance(vn_node.value, str)
        ):
            return

        verbose_name = vn_node.value
        if not verbose_name[0].isupper():
            return
        if any(verbose_name.startswith(acronym) for acronym in KNOWN_ACRONYMS):
            return
        yield self.make_error(
            "`{name}` verbose name `{verbose_name}` should not be capitalized",
            params={
                "name": context_name,
                "verbose_name": verbose_name,
            },
            node=vn_node,
        )


class FieldVerboseNameCapitalization(BaseVerboseNameCapitalizationCheck):
    id = "field-verbose-name-capitalization"
    description = """Check that field verbose_names are not capitalized"""

    def check(self):
        for cdef, assign in find_all_model_fields(self.context, self.file_context.ast):
            field_kwargs = get_call_kwargs(assign.value)
            vn_node = field_kwargs.get("verbose_name")
            yield from self._check_verbose_name(
                context_name=assign.targets[0], vn_node=vn_node
            )


class ModelVerboseNameCapitalization(BaseVerboseNameCapitalizationCheck):
    id = "model-verbose-name-capitalization"
    description = """Check that model verbose_names are not capitalized"""

    def check(self):
        for cdef in find_all_model_definitions(self.context, self.file_context.ast):
            assignments = get_model_meta_assignments(cdef)
            for field in ("verbose_name", "verbose_name_plural"):
                if field in assignments:
                    vn_node = assignments[field]
                    if (
                        vn_node
                        and isinstance(vn_node, Const)
                        and isinstance(vn_node.value, str)
                    ):
                        yield from self._check_verbose_name(
                            context_name=cdef.name, vn_node=vn_node
                        )
