import setuptools
import fastentrypoints  # noqa

dev_dependencies = [
    'autopep8',
    'flake8',
    'isort',
    'pytest~=3.2.0',
    'pytest-cov',
]

if __name__ == '__main__':
    setuptools.setup(
        name='django-lint',
        description='Statically analyze Django projects for common problems.',
        version='0.0.0',
        url='https://github.com/akx/django-lint',
        author='Aarni Koskela',
        maintainer='Aarni Koskela',
        maintainer_email='akx@iki.fi',
        license='MIT',
        install_requires=['astroid~=1.5.0'],
        extras_require={'dev': dev_dependencies},
        packages=setuptools.find_packages('.', include=('django_lint*',)),
        entry_points={'console_scripts': ['django-lint=django_lint.cli:cli']},
        include_package_data=True,
    )
