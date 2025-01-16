from setuptools import setup, find_packages

setup(
    name="nrc",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "numpy",
        "scipy",
        "pandas",
    ],
)
