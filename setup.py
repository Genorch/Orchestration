import os
from setuptools import setup

with open('requirements.txt') as f:
        required = f.read().splitlines()


setup(
    name='genorch',
    version='0.0.1',
    py_modules=['genorch'],
    include_package_data=True,
    install_requires=required,
    entry_points='''
        [console_scripts]
        genorch_serve=genorch:cli
    '''
)
