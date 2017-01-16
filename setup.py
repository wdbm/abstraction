#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import setuptools

def main():

    setuptools.setup(
        name             = "abstraction",
        version          = "2017.01.16.1534",
        description      = "machine learning framework",
        long_description     = long_description(),
        url              = "https://github.com/wdbm/abstraction",
        author           = "Will Breaden Madden",
        author_email     = "wbm@protonmail.ch",
        license          = "GPLv3",
        py_modules       = [
                           "abstraction"
                           ],
        install_requires = [
                           "bs4",
                           "dataset",
                           "datavision",
                           "flask",
                           "numpy",
                           "matplotlib",
                           "praw",
                           "propyte",
                           "pyprel",
                           "skflow",
                           "sklearn",
                           "shijian",
                           "technicolor",
                           "tonescale"
                           ],
        scripts          = [
                           "abstraction_interface.py"
                           ],
        entry_points     = """
            [console_scripts]
            abstraction = abstraction:abstraction
        """
    )

def long_description(
    filename = "README.md"
    ):

    if os.path.isfile(os.path.expandvars(filename)):
        try:
            import pypandoc
            long_description = pypandoc.convert_file(filename, "rst")
        except ImportError:
            long_description = open(filename).read()
    else:
        long_description = ""
    return long_description

if __name__ == "__main__":
    main()