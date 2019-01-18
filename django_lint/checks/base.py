from typing import Optional

from django_lint.errors import Error


class Check:
    id = None
    description = ""
    run_on_migrations = False

    def __init__(self, file_context):
        """
        :type file_context: django_lint.contexts.FileContext
        """
        self.file_context = file_context

    def check(self):
        raise NotImplementedError('{cls} must implement check()'.format(cls=self.__class__.__name__))

    def make_error(self, message, params: Optional[dict] = None, *, code=None, node=None):
        if params is None:
            params = {}
        return Error(
            check=self,
            file_context=self.file_context,
            message=message,
            params=params,
            code=code,
            node=node,
        )

    @property
    def context(self):
        return self.file_context.context
