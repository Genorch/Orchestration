from setuptools import setup, find_packages

with open('requirements.txt') as f:
        required = f.read().splitlines()


setup(
    name='genorch',
    version='0.0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    entry_points='''
        [console_scripts]
        genorch=genorch_serve:cli
    ''',
)
