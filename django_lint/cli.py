import argparse

from django_lint.checks.registry import get_check_classes
from django_lint.contexts import Context, FileContext
from django_lint.files import collect_files

ap = argparse.ArgumentParser()
ap.add_argument('target', nargs='+')
ap.add_argument('--disable', '-d', action='append', nargs='*', default=())


def cli(args=None):
    args = ap.parse_args(args)
    files = set(f for f in collect_files(targets=args.target) if f.endswith('.py'))
    context = Context(files=sorted(files))
    check_classes = {c for c in get_check_classes() if c.id not in args.disable}

    for filename in context.files:
        file_context = FileContext(context, filename)
        for check_cls in check_classes:
            if file_context.is_migration and not check_cls.run_on_migrations:
                continue

            errors = check_cls(file_context).check()
            if errors is None:
                continue
            for error in errors:
                print(error)
