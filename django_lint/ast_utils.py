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
