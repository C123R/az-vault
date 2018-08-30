import os
from setuptools import setup, find_packages

setup(
    name='azvault',
    version='0.1',
    py_modules=['azvault'],
    install_requires=[
        'Click',
        'azure-mgmt-keyvault',
        'haikunator',   
        'keyring',
        'azure-keyvault',
    ],
    entry_points='''
        [console_scripts]
        azvault=azvault:cli
    ''',
)
