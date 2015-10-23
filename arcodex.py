#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# arcodex: archive collated exchanges                                          #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is a data collation and archiving program specialised to        #
# conversational exchanges.                                                    #
#                                                                              #
# copyright (C) 2014 William Breaden Madden                                    #
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

Usage:
    program [options]

Options:
    -h, --help                   display help message
    --version                    display version and exit
    -v, --verbose                verbose logging
    -s, --silent                 silent
    -u, --username=USERNAME      username
    -r, --subreddits=SUBREDDITS  subreddits [default: changemyview]
    -n, --numberOfUtterances=N   number of utterances to access [default: 10]
    -d, --database=FILE          database [default: database.db]
"""

name    = "arcodex"
version = "2015-10-23T1450Z"
logo    = None

import os
import sys
import subprocess
import time
import datetime
import logging
import inspect
import docopt
import dataset
import praw
import propyte
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

    # access options and arguments
    subreddits         = options["--subreddits"].split(",")
    numberOfUtterances = options["--numberOfUtterances"]
    database           = options["--database"]

    log.info("access exchanges")
    exchangesReddit = abstraction.access_exchanges_Reddit(
        userAgent          = name,
        subreddits         = subreddits,
        numberOfUtterances = numberOfUtterances
    )
    log.info("save exchanges to database (only those not saved previously)")
    abstraction.save_exchanges_to_database(
        exchanges = exchangesReddit,
        fileName  = database
    )
    abstraction.save_database_metadata(
        fileName = database
    )

    program.terminate()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
