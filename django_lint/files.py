import os

SKIPPED_DIRS = {
    '.awcache',
    '.cache',
    '.git',
    '.idea',
    '__pycache__',
    'node_modules',
    '.mypy_cache',
}

SKIPPED_PATH_SEGMENTS = {
    'var/media',
    'var/static',
    '.tox',
    'site-packages',
}


def collect_files(targets):
    for target in targets:
        if os.path.isdir(target):
            for dirpath, dirnames, filenames in os.walk(target):
                dirnames[:] = [
                    dirname
                    for dirname
                    in dirnames
                    if not (
                        dirname in SKIPPED_DIRS or
                        any(seg in os.path.join(dirpath, dirname) for seg in SKIPPED_PATH_SEGMENTS)
                    )
                ]
                yield from (os.path.realpath(os.path.join(dirpath, filename)) for filename in filenames)
        else:
            yield os.path.realpath(target)
