#!/usr/bin/env python3

import io
import os
import mhl_to_csv
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

setup(
    name='mhl_to_csv',
    version=mhl_to_csv.__version__,
    author='ltocsvparser.__author__',
    author_email='joshunwin@gmail.com',
    description='Converts one or more MHL files into a single CSV',
    py_modules=['mhl_to_csv'],
    entry_points={  # Optional
        'console_scripts': [
            'mhl_to_csv=mhl_to_csv:main',
        ],
    },
    platforms='macOS',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Console',
        'License :: OSI Approved :: '
        'GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Networking'])
