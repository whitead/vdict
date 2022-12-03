from glob import glob
from setuptools import setup

exec(open("vdict/version.py").read())

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vdict",
    version=__version__,
    description="A dict with a vector index for fast lookup of nearest neighbors",
    author="Andrew White",
    author_email="andrew.white@rochester.edu",
    url="https://github.com/ur-whitelab/vdict",
    license="MIT",
    packages=["vdict"],
    install_requires=[
        "hnswlib",
    ],
    test_suite="tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
