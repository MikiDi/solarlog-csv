# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="solarlog-csv",
    version="0.1.0",
    description="A Python utility for converting Solar-Log data into csv-files",
    license="MIT",
    url='https://github.com/MikiDi/solarlog-csv',
    author='Michaël Dierick',
    author_email='michael@dierick.io',
    scripts=['bin/solarlog-csv'],
    packages=find_packages(),
    install_requires=["pytz"],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License"
    ]
)
