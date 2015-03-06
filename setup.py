"""Setuptools configuration for confpy."""

from setuptools import setup
from setuptools import find_packages


with open('README.rst', 'r') as readmefile:

    README = readmefile.read()

with open('requirements.txt', 'r') as reqfile:

    REQUIREMENTS = reqfile.readlines()

with open('LICENSE', 'r') as licensefile:

    LICENSE = licensefile.readlines()

setup(
    name='confpy',
    version='0.8.0',
    url='https://github.com/kevinconway/confpy',
    description='Config file parsing and option management.',
    author="Kevin Conway",
    author_email="kevinjacobconway@gmail.com",
    long_description=README,
    license=LICENSE,
    packages=find_packages(exclude=['tests', 'build', 'dist', 'docs']),
    requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'confpy-generate = confpy.cmd:generate_example',
        ],
    },
    include_package_data=True,
)
