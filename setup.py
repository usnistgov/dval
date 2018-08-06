try: # for pip >= 10
    import pip._internal as pip
except ImportError: # for pip <= 9.0.3
    import pip
import sys
import os
from setuptools import setup
import d3m_outputs

PACKAGE_NAME = 'd3m_outputs'
MINIMUM_PYTHON_VERSION = 3, 6


def check_python_version():
    """Exit when the Python version is too low."""
    if sys.version_info < MINIMUM_PYTHON_VERSION:
        sys.exit("Python {}.{}+ is required.".format(*MINIMUM_PYTHON_VERSION))


def read_package_variable(key):
    """Read the value of a variable from the package without importing."""
    module_path = os.path.join(PACKAGE_NAME, '__init__.py')
    with open(module_path) as module:
        for line in module:
            parts = line.strip().split(' ')
            if parts and parts[0] == key:
                return parts[-1].strip("'")
    assert False, "'{0}' not found in '{1}'".format(key, module_path)


def parse_requirements():
    """Parse requirements.txt
    """
    requires, links = [], []

    requirements = pip.req.parse_requirements(
        'requirements.txt', session=pip.download.PipSession())

    for item in requirements:
        # we want to handle package names and also repo urls
        if getattr(item, 'url', None):  # older pip has url
            links.append(str(item.url))
        if getattr(item, 'link', None):  # newer pip has link
            links.append(str(item.link))
        if item.req:
            requires.append(str(item.req))

    return requires, links


check_python_version()
requires, links = parse_requirements()

setup(install_requires=requires,
      version=d3m_outputs.__version__,
      entry_points='''
          [console_scripts]
          d3moutputs=d3m_outputs.cli:main
          d3m_outputs=d3m_outputs.cli:main
      ''')
