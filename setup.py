# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = "1.0.0"

setup(
    name="senaite.serial.cli",
    version=version,
    description="Command line interface for RS-232 devices",
    long_description=open("README.rst").read(),
    long_description_content_type="text/markdown",
    license="GPLv2",
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords=["senaite", "lims", "rs-232", "astm"],
    author="RIDING BYTES & NARALABS",
    author_email="senaite@senaite.com",
    url="https://github.com/senaite/senaite.serial.cli",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=["senaite", "senaite.serial"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "pyserial",
    ],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        "dev": [
            "pytest",
            "coverage",
        ]
    },
    entry_points={
        "console_scripts": ["senaite_serial=senaite.serial.cli.app:main"]
    }
)
