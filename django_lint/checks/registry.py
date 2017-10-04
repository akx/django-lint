import os
from importlib import import_module

from django_lint.checks.base import Check


def import_builtin_check_modules():
    excluded_modnames = {'__init__', 'base', 'registry'}
    for file in os.listdir(os.path.dirname(__file__)):
        modname = os.path.splitext(file)[0]
        if file.endswith('.py') and modname not in excluded_modnames:
            import_module('.' + modname, 'django_lint.checks')


def get_check_classes():
    import_builtin_check_modules()
    check_classes = set()

    def walk(cls):
        if cls.id:
            check_classes.add(cls)
        for cls in cls.__subclasses__():
            walk(cls)

    walk(Check)
    return check_classes
