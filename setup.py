# coding: utf-8
from setuptools import setup, find_packages

setup(
    name='csp-reporter',
    version='1.1.1',
    description='Parser for CSP (Content Security Policy) reports',
    author='oxdef',
    author_email='oxdef@oxdef.info',
    url='https://oxdef.info/csp-reporter',
    packages=find_packages(),
    scripts=['csp-reporter.py'],
    include_package_data=True,
    install_requires=[
        'Jinja2'
    ]
    )
