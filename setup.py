#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import setuptools

def main():

    setuptools.setup(
        name             = "abstraction",
        version          = "2018.01.11.2110",
        description      = "machine learning framework",
        long_description = long_description(),
        url              = "https://github.com/wdbm/abstraction",
        author           = "Will Breaden Madden",
        author_email     = "wbm@protonmail.ch",
        license          = "GPLv3",
        py_modules       = [
                           "abstraction"
                           ],
        install_requires = [
                           "beautifulsoup4",
                           "dataset",
                           "datavision",
                           "docopt",
                           "flask",
                           "jupyter",
                           "lxml",
                           "numpy",
                           "matplotlib",
                           "praw",
                           "propyte",
                           "pyprel",
                           "shijian",
                           "sklearn",
                           "technicolor",
                           "tmux_control",
                           "tonescale"
                           ],
        scripts          = [
                           "abstraction_generate_response.py",
                           "abstraction_interface.py",
                           "gpudeets.py"
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
