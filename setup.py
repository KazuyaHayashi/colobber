#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="colobber",
    version="0.0.1",
    description="Colobber the board game",
    author="Hayashi Kazuya",
    author_email="pumpkin.brownies@gmail.com",
    url="",
    packages=find_packages(),
    entry_points={"console_scripts": "colobber = src.main:main"}
)