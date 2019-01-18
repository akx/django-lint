from astroid import ClassDef

from django_lint.ast_utils import (find, get_classdef_field_names, is_admin_definition)
from django_lint.checks.base import Check


class AdminShouldHaveSearchFields(Check):
    id = 'admin-search-fields'
    description = """Check that admin classes define search_fields"""

    def check(self):
        ast = self.file_context.ast
        for cdef in find(ast, type=ClassDef):
            if is_admin_definition(self.context, cdef):
                field_names = set(get_classdef_field_names(cdef))
                if 'search_fields' not in field_names:
                    yield self.make_error(
                        'Admin class {name} missing `search_fields`',
                        {'name': cdef.name},
                        node=cdef,
                    )
