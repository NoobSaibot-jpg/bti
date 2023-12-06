from setuptools import setup, find_packages
import py2exe

setup(
    name='bti',
    version='0.1.2',
    packages=find_packages(),
    console=['img_read.py']
)
