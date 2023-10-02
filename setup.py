from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="type-strict",
    version="0.1.0",
    description="Python's missing runtime type checker",
    url='https://github.com/Alex0Blackwell/type-strict',
    author="Alex Blackwell",
    author_email="alex.blackwell314@gmail.com",
    license="MIT",
    packages=["type_strict"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
