import argparse
import os
import sys

import astroid

from django_lint.checks.registry import get_check_classes
from django_lint.contexts import Context, FileContext
from django_lint.files import collect_files

parser = argparse.ArgumentParser()
parser.add_argument("target", nargs="*")
parser.add_argument(
    "--list-checks", "-l", action="store_true", help="list checks, then exit"
)
parser.add_argument("--disable", "-d", action="append", help="disable these checks")
parser.add_argument("--only", action="append", help="enable only these checks")
parser.add_argument(
    "--fast",
    action="store_true",
    help="tell checks to try and be faster (though less accurate)",
)
parser.add_argument(
    "--prepend-to-path",
    "-p",
    action="append",
    help="prepend this to `sys.path` – allows analysis to find libraries that might be in other venvs",
)


def check_file(context, filename, check_classes):
    file_context = FileContext(context, filename)
    for check_cls in check_classes:
        if file_context.is_migration and not check_cls.run_on_migrations:
            continue

        errors = check_cls(file_context).check()
        if errors is None:
            continue
        for error in errors:
            print(error)


def is_check_enabled(cls, only, disable):
    if only:
        return cls.id in only
    return cls.id not in (disable or ())


def cli(args=None):
    args = parser.parse_args(args)
    if args.list_checks:
        for check in sorted(get_check_classes(), key=lambda c: c.id):
            print(check.id)
        return

    prepend_to_path = list(args.prepend_to_path or ())
    assert all(
        os.path.isdir(d) for d in prepend_to_path
    ), "all prepend-to-path entries must be directories"
    sys.path[:] = list(prepend_to_path) + sys.path

    files = set(f for f in collect_files(targets=args.target) if f.endswith(".py"))
    context = Context(files=sorted(files), fast=args.fast)
    check_classes = {
        c
        for c in get_check_classes()
        if is_check_enabled(c, only=args.only, disable=args.disable)
    }

    for filename in context.files:
        try:
            check_file(context, filename, check_classes)
        except astroid.exceptions.AstroidSyntaxError as ase:
            print("Unable to parse %s: %s" % (filename, ase), file=sys.stderr)
