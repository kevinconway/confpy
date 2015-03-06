"""Setuptools configuration for confpy."""

from setuptools import setup
from setuptools import find_packages


with open('README.rst', 'r') as readmefile:

    README = readmefile.read()

setup(
    name='confpy',
    version='0.9.3',
    url='https://github.com/kevinconway/confpy',
    description='Config file parsing and option management.',
    author="Kevin Conway",
    author_email="kevinjacobconway@gmail.com",
    long_description=README,
    license='MIT',
    packages=find_packages(exclude=['tests', 'build', 'dist', 'docs']),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'confpy-generate = confpy.cmd:generate_example',
        ],
    },
    include_package_data=True,
)
