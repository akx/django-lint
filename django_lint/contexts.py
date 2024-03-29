import os

from astroid import MANAGER as astroid_manager
from lazy_object_proxy.utils import cached_property


class Context:
    def __init__(self, files, fast=False):
        self.files = files
        self.fast = bool(fast)

    @cached_property
    def files_common_prefix(self):
        return os.path.commonprefix(self.files)


class FileContext:
    def __init__(self, context, path):
        self.context = context
        self.path = path

    @cached_property
    def ast(self):
        return astroid_manager.ast_from_file(self.path)

    @cached_property
    def relative_path(self):
        return self.path[len(self.context.files_common_prefix) :]

    @cached_property
    def is_migration(self):
        return os.path.dirname(self.path).endswith("migrations")
