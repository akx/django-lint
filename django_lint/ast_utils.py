from astroid import ClassDef, Assign, Call
from astroid.node_classes import NodeNG


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


def is_model_definition(cdef: ClassDef):
    # TODO: Could be improved, probably :)
    return any(base._repr_name().endswith('Model') for base in cdef.bases)


def find_all_model_fields(ast):
    for cdef in find(ast, type=ClassDef):  # Find all class definitions
        if not is_model_definition(cdef):  # If the class does not smell like a model, never mind
            continue
        # Find all assignments whose rvalue is a call
        for assign in find(cdef, type=Assign, attrs={'value': lambda n, v: isinstance(v, Call)}):
            yield (cdef, assign)


def get_call_kwargs(call):
    return {kw.arg for kw in (call.keywords or ())}
