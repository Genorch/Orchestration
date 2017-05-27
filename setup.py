from setuptools import setup

setup(
    name='genorch',
    version='0.1',
    py_modules=['genorch'],
    install_requires=[
        'python-novaclient',
        'ansible',
        'click',
        'pyyaml'
    ],
    entry_points='''
        [console_scripts]
        genorch=genorch_serve:cli
    '''
)
