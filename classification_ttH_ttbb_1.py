#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# classification_ttH_ttbb_1                                                    #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is for classification training on ttH and ttbb HEP MC           #
# events.                                                                      #
#                                                                              #
# copyright (C) 2015 William Breaden Madden                                    #
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
    -h, --help               display help message
    --version                display version and exit
    -v, --verbose            verbose logging
    -s, --silent             silent
    -u, --username=USERNAME  username
    --datattH=FILENAME       input ROOT data file [default: output_ttH.root]
    --datattbb=FILENAME      input ROOT data file [default: output_ttbb.root]
"""
from __future__ import division

name    = "classification_ttH_ttbb_1"
version = "2015-12-16T1444Z"
logo    = name

import os
import sys
import time
import docopt
import logging
import propyte
import shijian
import datavision
import abstraction

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

    log.info("")

    # access options and arguments
    ROOT_filename_ttH = options["--datattH"]
    ROOT_filename_ttbb = options["--datattbb"]

    log.info("ttH data file: {filename}".format(
        filename = ROOT_filename_ttH
    ))
    log.info("ttbb data file: {filename}".format(
        filename = ROOT_filename_ttbb
    ))

    # upcoming

    # Access data for event classes ttbb and ttH and add class labels to them.

    data = abstraction.load_HEP_data(
        ROOT_filename            = "output.root",
        tree_name                = "nominal",
        maximum_number_of_events = None
        )
    print(data.table())

    # Combine the data sets and prepare them for classifier training.

    log.info("")

    program.terminate()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
