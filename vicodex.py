#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# vicodex                                                                      #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is a database inspection program specialised to conversational  #
# exchanges.                                                                   #
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
    -h, --help               display help message
    --version                display version and exit
    -v, --verbose            verbose logging
    -s, --silent             silent
    -u, --username=USERNAME  username
    -d, --database=FILE      database [default: database.db]
    -t, --tableLimit=NUMBER  limit on number of table entries displayed
    -t, --outputFile=NAME    optional output file for simple training
"""

name    = "vicodex"
version = "2016-01-18T1611Z"
logo    = None

import os
import sys
import subprocess
import time
import datetime
import logging
import inspect
import dataset
import abstraction
import docopt
import technicolor
import shijian
import propyte
import pyprel

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
    table_limit       = options["--tableLimit"]
    if table_limit is not None:
        table_limit = int(table_limit)
    output_filename   = options["--outputFile"]
    if output_filename is not None:
        output_filename = str(output_filename)

    # Access database.
    database = abstraction.access_database(filename = database_filename)
    log.info("\ndatabase metadata:")
    abstraction.log_database_metadata(filename = database_filename)
    log.info("")
    # Print the tables in the database.
    log.info("tables in database: {tables}".format(
        tables = database.tables
    ))
    # Access the exchanges table.
    table_name = "exchanges"
    log.info("access table \"{table_name}\"".format(
        table_name = table_name
    ))
    # Print the columns of the table.
    log.info("columns in table \"{table_name}\": {columns}".format(
        table_name = table_name,
        columns    = database[table_name].columns
    ))
    # Print the number of rows of the table.
    log.info("number of rows in table \"{table_name}\": {number_of_rows}".format(
        table_name     = table_name,
        number_of_rows = str(len(database[table_name]))
    ))
    # Print the table entries:
    log.info("entries of table {table_name}:\n".format(
        table_name    = table_name
    ))
    # Define table headings.
    table_contents = [
        [
            "id",
            "utterance",
            "response",
            "utteranceTimeUNIX",
            "responseTimeUNIX",
            "utteranceReference",
            "responseReference",
            "exchangeReference"
        ]
    ]
    simple_training_representation = ""
    # Fill table data.
    count_entries = 0
    for entry in database[table_name].all():
        table_contents.append(
            [
                str(entry["id"]),
                str(entry["utterance"]),
                str(entry["response"]),
                str(entry["utteranceTimeUNIX"]),
                str(entry["responseTimeUNIX"]),
                str(entry["utteranceReference"]),
                str(entry["responseReference"]),
                str(entry["exchangeReference"])
            ]
        )
        count_entries += 1
        # simple training representation
        if output_filename is not None:
            if simple_training_representation is "":
                simple_training_representation = \
                    str(entry["utterance"]) + \
                    " => " + \
                    str(entry["response"])
            else:
                simple_training_representation = \
                    simple_training_representation + \
                    "\n" + \
                    str(entry["utterance"]) + \
                    " => " + \
                    str(entry["response"])
        if table_limit is not None:
            if count_entries >= table_limit:
                break
    # Record table.
    print(
        pyprel.Table(
            contents = table_contents
        )
    )
    # Record to file, if specified.
    if output_filename is not None:
        log.info(
            "save simple training representation to file {filename}".format(
                filename = output_filename
            )
        )
        output_file = open(output_filename, "w")
        output_file.write(simple_training_representation)
        output_file.close()

    program.terminate()

if __name__ == "__main__":

    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
