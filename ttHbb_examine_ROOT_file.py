#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# ttHbb_examine_ROOT_file                                                      #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program examines a ROOT file.                                           #
#                                                                              #
# copyright (C) 2017 William Breaden Madden                                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################

usage:
    program [options]

options:
    -h, --help               Show this help message.
    --version                Show the version and exit.
    -v, --verbose            Show verbose logging.
    -s, --silent             silent
    -u, --username=USERNAME  username

    --fileroot=FILENAME      ROOT file  [default: output.root]
    --tree=TEXT              tree name  [default: nominal_Loose]
"""

from __future__ import division
import docopt
import os
import textwrap

import abstraction
import propyte
with propyte.import_ganzfeld():
    from ROOT import *
import shijian

name    = "ttHbb_examine_ROOT_file"
version = "2017-04-21T0117Z"
logo    = name

def main(options):

    global program
    program = propyte.Program(
        options = options,
        name    = name,
        version = version,
        logo    = logo
    )
    global log
    from propyte import log

    print("")

    filename_ROOT = options["--fileroot"]
    name_tree     = options["--tree"]

    if not os.path.isfile(os.path.expandvars(filename_ROOT)):
        log.error("file {filename} not found".format(
            filename = filename_ROOT
        ))
        program.terminate()

    file_ROOT       = abstraction.open_ROOT_file(filename_ROOT)
    tree            = file_ROOT.Get(name_tree)

    number_entries  = tree.GetEntries()
    names_variables = [variable.GetName() for variable in tree.GetListOfBranches()]
    names_variables = shijian.natural_sort(names_variables)
    names_objects   = [key.GetName() for key in file_ROOT.GetListOfKeys()]
    names_objects   = shijian.natural_sort(names_objects)

    log.info(textwrap.dedent(
        """
        input ROOT file:   {filename_ROOT}
        number of entries: {number_entries}
        """.format(
            filename_ROOT  = filename_ROOT,
            number_entries = number_entries
        )
    ))

    log.info("variables:")
    print("")
    for name_variable in names_variables:
        log.info("    " + name_variable)

    print("")
    log.info("objects:")
    print("")
    for name_object in names_objects:
        log.info("    " + name_object)

    #print("")
    #log.info("tree printout:")
    #print("")
    #tree.Print()
    #print("")

    program.terminate()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
