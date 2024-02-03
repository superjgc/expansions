from setuptools import setup, find_packages

setup(
    name='expansions',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        "pydantic==1.9.1",
        "SQLAlchemy==1.4.39",
        "humps==0.2.2"
    ]
)
