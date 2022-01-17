# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py
# https://github.com/pypa/sampleproject/blob/main/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='TMDB lookup',
    version='0.1.0',
    description='Query TheMovieDataBase for data',
    long_description=readme,
    author='Jean-Carol Forato',
    author_email='jcfrt@free.fr',
    url='https://github.com/jcfrt/tmdb_query',
    license=license,
    packages=find_packages(exclude=('test',)),
    python_requires='>=3.8, <4',
    install_requires=['requests'],
    extras_require={
        'test': ['pytest']
    },
)
