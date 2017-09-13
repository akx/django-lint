from astroid import Call

from django_lint.ast_utils import find_all_model_fields, get_call_kwargs
from django_lint.checks.base import Check


def smells_like_related_field(node):
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


class RelatedFieldExplicitOnDeleteCheck(Check):
    id = 'related-field-explicit-on-delete'
    description = """
    Check that all RelatedFields (ForeignKeys, ManyToManyFields and OneToOneFields) have
    an explicit `on_delete` clause.
    """

    def check(self):
        for cdef, assign in find_all_model_fields(self.context, self.file_context.ast):
            if not smells_like_related_field(assign.value):
                continue
            if 'on_delete' not in get_call_kwargs(assign.value):
                yield self.make_error(
                    '{field_type} `{name}` missing explicit `on_delete`',
                    {
                        'field_type': assign.value.func,
                        'name': assign.targets[0],
                    },
                    node=assign,
                )


class RelatedFieldExplicitRelatedNameCheck(Check):
    id = 'related-field-explicit-related-name'
    description = """
    Check that all RelatedFields (ForeignKeys, ManyToManyFields and OneToOneFields) have
    an explicit `related_name`.
    """

    def check(self):
        for cdef, assign in find_all_model_fields(self.context, self.file_context.ast):
            if not smells_like_related_field(assign.value):
                continue
            if 'related_name' not in get_call_kwargs(assign.value):
                yield self.make_error(
                    '{field_type} `{name}` missing explicit `related_name`',
                    {
                        'field_type': assign.value.func,
                        'name': assign.targets[0],
                    },
                    node=assign,
                )
