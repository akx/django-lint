import os

SKIPPED_DIRS = {
    '.git',
    '__pycache__',
    'node_modules',
}


def collect_files(targets):
    for target in targets:
        if os.path.isdir(target):
            for dirpath, dirnames, filenames in os.walk(target):
                dirnames[:] = [dirname for dirname in dirnames if dirname not in SKIPPED_DIRS]
                yield from (os.path.realpath(os.path.join(dirpath, filename)) for filename in filenames)
        else:
            yield os.path.realpath(target)
