from astroid import ClassDef, Assign, Call

from django_lint.ast_utils import find
from django_lint.checks.base import Check


def smells_like_foreign_key(node):
    if isinstance(node, Call):
        field_type_name = node.func._repr_name()
    else:
        field_type_name = node._repr_name()
    if field_type_name.endswith('ForeignKey'):
        return True
    if field_type_name.endswith('ManyToManyField'):
        return True
    if field_type_name.endswith('OneToOneField'):
        return True


class ForeignKeyOnDeleteCheck(Check):
    id = 'foreign-key-explicit-on-delete'

    def check(self):
        if 'migrations/' in self.file_context.path:
            return
        for cdef in find(self.file_context.ast, type=ClassDef):  # Find all class definitions
            if not any(base._repr_name().endswith('Model') for base in cdef.bases):
                # If the class does not smell like a model, never mind
                continue
            # Find all assignments whose rvalue is a call
            for assign in find(cdef, type=Assign, attrs={'value': lambda n, v: isinstance(v, Call)}):
                if not smells_like_foreign_key(assign.value):
                    continue
                if 'on_delete' not in {kw.arg for kw in (assign.value.keywords or ())}:
                    yield self.make_error(
                        'Call to {field} missing explicit `on_delete`',
                        {'field': assign.value.func},
                        node=assign,
                    )
