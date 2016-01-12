#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# inspect-database                                                             #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program gives a simple printout of a database.                          #
#                                                                              #
# 2015 Will Breaden Madden, w.bm@cern.ch                                       #
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
    -h, --help               display help message
    --version                display version and exit
    -v, --verbose            verbose logging
    -s, --silent             silent
    -u, --username=USERNAME  username
    -d, --database=FILE      database [default: database.db]
"""

name    = "inspect-database"
version = "2016-01-12T2037Z"
logo    = None

import os
import sys
import logging
import docopt
import technicolor
import shijian
import pyprel
import propyte
import abstraction

@shijian.timer
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
    database_filename = options["--database"]

    log.info("")

    database = abstraction.access_database(
        filename = database_filename
    )

    for table in database.tables:
        log.info("\ntable: {table}/n".format(
            table = table
        ))
        for entry in database[table].all():
            pyprel.print_line()
            for column in database[table].columns:
                log.info("\n{column}: {content}".format(
                    column  = column,
                    content = str(entry[column])
                ))
        pyprel.print_line()

    log.info("")

    program.terminate()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
