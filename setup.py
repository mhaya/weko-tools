import os, sys
from setuptools import setup, find_packages

def read_requirements():
    """Parse requirements from requirements.txt."""
    reqs_path = os.path.join('.', 'requirements.txt')
    with open(reqs_path, 'r') as f:
        requirements = [line.rstrip() for line in f]
    return requirements

setup(
    name='weko-tools',
    version='0.0.1',
    description='weko-tools',
    long_description='readme',
    author='Masaharu Hayashi',
    author_email='masaharu.hayashi3@gmail.com',
    install_requires=read_requirements(),
    dependency_links=['git+ssh://git@github.com/mhaya/weko-tools.git#egg=weko-tools'],
    url='https://github.com/mhaya/weko-tools',
    license='license',
    packages=find_packages(exclude=('tests', 'docs')),
    test_suite='tests'
)
