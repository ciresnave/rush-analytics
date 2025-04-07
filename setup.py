from pathlib import Path

from setuptools import find_packages, setup

setup(
    name="rush-analytics",
    version="0.1.0",
    author="Eric Evans",
    author_email="Eric.Evans@EvansLaboratories.com",
    description="A Python client for Rush Analytics API",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url='https://github.com/CireSnave/rush-analytics',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)