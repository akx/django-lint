import re

from astroid import ClassDef, Assign, Call
from astroid.helpers import safe_infer
from astroid.node_classes import NodeNG

from django_lint.contexts import Context


def _check_attr(obj, key, expected):
    value = getattr(obj, key, None)
    if value == expected:
        return True
    if callable(expected):
        return expected(obj, value)
    return False


# noinspection PyDefaultArgument
def find(root, *, type=None, attrs={}, depth=10000):
    """
    Recursively find AST nodes that match the given spec.

    :type root: astroid.node_classes.NodeNG
    :type type: class
    :type attrs: dict[str, object]
    :return:
    """
    for child in root.get_children():
        assert isinstance(child, NodeNG)
        match = True
        if type and not isinstance(child, type):
            match = False
        if not all(_check_attr(child, key, value) for (key, value) in attrs.items()):
            match = False
        if match:
            yield child
        if depth > 0:
            yield from find(child, type=type, attrs=attrs, depth=(depth - 1))


def as_re_pattern(regexp, flags=0):
    if isinstance(regexp, re.Pattern):
        return regexp
    return re.compile(regexp, flags=flags)


def get_classdef_inheritance_checker(
    fast_base_regexps=(),
    slow_base_qname_regexps=(),
):
    fast_base_regexps = [as_re_pattern(re) for re in fast_base_regexps]
    slow_base_qname_regexps = [as_re_pattern(re) for re in slow_base_qname_regexps]

    def check_classdef(context: Context, cdef: ClassDef):
        # Fast path: look at classes that smell like models
        if fast_base_regexps and any(
            any(r.search(base._repr_name()) for r in fast_base_regexps)
                for base in cdef.bases
        ):
            return True

        # Slower path: run inference and look at ancestor classes
        if not context.fast:
            if slow_base_qname_regexps and any(
                any(r.search(anc.qname()) for r in slow_base_qname_regexps)
                    for anc in safe_infer(cdef).ancestors()
            ):
                return True

        return False

    return check_classdef


is_model_definition = get_classdef_inheritance_checker(
    fast_base_regexps=(r'Model$',),
    slow_base_qname_regexps=(re.escape('django.db.models.base.Model'),),
)


def find_all_model_definitions(context: Context, ast: NodeNG):
    for cdef in find(ast, type=ClassDef):  # Find all class definitions
        if not is_model_definition(context, cdef):  # If the class does not smell like a model, never mind
            continue
        yield cdef


def find_all_model_fields(context: Context, ast: NodeNG):
    for cdef in find_all_model_definitions(context, ast):
        # Find all assignments whose rvalue is a call
        for assign in find(cdef, type=Assign, attrs={'value': lambda n, v: isinstance(v, Call)}):
            yield (cdef, assign)


def get_call_kwargs(call):
    return {kw.arg: kw.value for kw in (call.keywords or ())}


def get_model_meta(cdef: ClassDef):
    try:
        return next(find(cdef, type=ClassDef, attrs={'name': 'Meta'}))
    except StopIteration:
        return None


def get_model_meta_assignments(cdef: ClassDef):
    meta = get_model_meta(cdef)
    assignments = {}
    if meta:
        for assign in find(meta, type=Assign):
            assignments[assign.targets[0].name] = assign.value
    return assignments
