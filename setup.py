from setuptools import setup, find_packages

setup(
    name="brag",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'brag=brag.main:cli',
        ],
    },
)
