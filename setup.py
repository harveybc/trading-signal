from setuptools import setup, find_packages

setup(
    name='trading_signal',
    version='0.1.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'trading_signal=app.main:main'
        ],
        'trading_signal.plugins': [
            'default_plugin=app.plugins.plugin_default:Plugin',
            'ls=app.plugins.plugin_ls:Plugin'
        ]
    },
    install_requires=[
        'pandas',
        'numpy'
    ],
    author='Harvey Bastidas',
    author_email='your.email@example.com',
    description='A training signal generation system that supports dynamic loading of plugins for processing CSV data.'
)
