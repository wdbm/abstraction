#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import setuptools
import pypandoc

def main():

    setuptools.setup(
        name             = "abstraction",
        version          = "2016.06.02.1354",
        description      = "machine learning framework",
        long_description = pypandoc.convert("README.md", "rst"),
        url              = "https://github.com/wdbm/abstraction",
        author           = "Will Breaden Madden",
        author_email     = "w.bm@cern.ch",
        license          = "GPLv3",
        py_modules       = [
                           "abstraction"
                           ],
        install_requires = [
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
                           "technicolor"
                           ],
        scripts          = [
                           "abstraction_interface.py"
                           ],
        entry_points     = """
            [console_scripts]
            abstraction = abstraction:abstraction
        """
    )

def read(*paths):
    with open(os.path.join(*paths), "r") as filename:
        return filename.read()

if __name__ == "__main__":
    main()
