from astroid import FunctionDef

from django_lint.ast_utils import find_all_model_definitions, find
from django_lint.checks.base import Check


class ModelExplicitStr(Check):
    id = 'model-explicit-str'
    description = """Check that all Models have __str__."""

    def check(self):
        for cdef in find_all_model_definitions(self.context, self.file_context.ast):
            if cdef.name.lower().endswith('mixin'):
                continue
            # TODO: Tbh, this should check the entire class hierarchy
            func_names = {fdef.name for fdef in find(cdef, type=FunctionDef, depth=1)}
            if '__str__' not in func_names:
                yield self.make_error(
                    'Model `{class_name}` missing `__str__`',
                    {
                        'class_name': cdef.name,
                    },
                    node=cdef,
                )
