import re
from io import StringIO
from operator import attrgetter
from textwrap import dedent

from django_lint.checks.registry import get_check_classes


def generate_readme_fragment():
    out_io = StringIO()
    for check_class in sorted(get_check_classes(), key=attrgetter("id")):
        out_io.write("### `{id}`\n\n".format(id=check_class.id))
        out_io.write(
            "{description}\n\n".format(
                description=dedent(check_class.description).strip()
            )
        )
    return out_io.getvalue()


def replace_readme_segment(old_readme, readme_fragment, start_re, end_re):
    start = start_re.search(old_readme)
    replace_from = start.span()[1]
    end = end_re.search(old_readme, start.span()[1])
    replace_to = end.span()[0]
    new_readme = (
        old_readme[:replace_from] + "\n" + readme_fragment + old_readme[replace_to:]
    )
    return new_readme


def main():
    start_re = re.compile("^## Checkers\n", re.MULTILINE)
    end_re = re.compile("^## ", re.MULTILINE)

    readme_fragment = generate_readme_fragment()

    with open("README.md", "r") as infp:
        old_readme = infp.read()

    new_readme = replace_readme_segment(old_readme, readme_fragment, start_re, end_re)

    with open("README.md", "w") as outfp:
        outfp.write(new_readme)


if __name__ == "__main__":
    main()
