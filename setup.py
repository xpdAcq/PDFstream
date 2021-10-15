import sys
from os import path

from setuptools import setup, find_packages

# NOTE: This file must remain Python 2 compatible for the foreseeable future,
# to ensure that we error out properly for people with outdated setuptools
# and/or pip.
min_version = (3, 7)
if sys.version_info < min_version:
    error = ("\n"
             "pdfstream does not support Python {0}.{1}.\n"
             "Python {2}.{3} and above is required. Check your Python version like so:\n"
             "\n"
             "python3 --version\n"
             "\n"
             "This may be due to an out-of-date pip. Make sure you have pip >= 9.0.1.\n"
             "Upgrade pip like so:\n"
             "\n"
             "pip install --upgrade pip\n").format(*(sys.version_info[:2] + min_version))
    sys.exit(error)

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

setup(
    name='pdfstream',
    version='0.5.0',
    description="The configs analysis toolbox for the study on pair distribution function (PDF).",
    install_requires=[],
    long_description=readme,
    long_description_content_type='text/markdown',
    author="Songsheng Tao",
    author_email='st3107@columbia.edu',
    url='https://github.com/xpdAcq/pdfstream',
    python_requires='>={}'.format('.'.join(str(n) for n in min_version)),
    packages=find_packages(exclude=['docs', 'tests']),
    entry_points={
        'console_scripts': [
            'pdfstream = pdfstream.main:main',
            'run_server = pdfstream.main:run_server',
            'print_server_config_dir = pdfstream.main:print_server_config_dir'
            # 'command = some.module:some_function',
        ],
    },
    include_package_data=True,
    package_data={
        'pdfstream': [
            'configs/*'
            # When adding files here, remember to update MANIFEST.in as well,
            # or else they will not be included in the distribution on PyPI!
            # 'path/to/data_file',
        ]
    },
    license="BSD (3-clause)",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    scripts=[
        'scripts/pdfstream_install'
    ]
)
