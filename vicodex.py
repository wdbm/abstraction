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
    -u, --username=USERNAME  username
    -d, --database=FILE      database [default: database.db]
    -t, --tableLimit=NUMBER  limit on number of table entries displayed
    -t, --outputFile=NAME    optional output file for simple training
"""

name    = "vicodex"
version = "2016-01-12T2212Z"

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
import pyprel

def main(options):

    global program
    program = Program(options = options)

    # Access database.
    database = abstraction.access_database(filename = program.database)
    log.info("\ndatabase metadata:")
    abstraction.log_database_metadata(filename = program.database)
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
        if program.output_file is not None:
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
        if program.table_limit is not None:
            if count_entries >= program.table_limit:
                break
    # Record table.
    print(
        pyprel.Table(
            contents = table_contents
        )
    )
    # Record to file, if specified.
    if program.output_file is not None:
        log.info(
            "save simple training representation to file {filename}".format(
                filename = program.output_file
            )
        )
        output_file = open(program.output_file, "w")
        output_file.write(simple_training_representation)
        output_file.close()

    program.terminate()

class Program(object):

    def __init__(
        self,
        parent  = None,
        options = None
        ):

        # internal options
        self.display_logo          = True

        # clock
        global clock
        clock = shijian.Clock(name = "program run time")

        # name, version, logo
        if "name" in globals():
            self.name              = name
        else:
            self.name              = None
        if "version" in globals():
            self.version           = version
        else:
            self.version           = None
        if "logo" in globals():
            self.logo              = logo
        elif "logo" not in globals() and hasattr(self, "name"):
            self.logo              = pyprel.render_banner(
                                         text = self.name.upper()
                                     )
        else:
            self.display_logo      = False
            self.logo              = None

        # options
        self.options               = options
        self.user_name             = self.options["--username"]
        self.database              = self.options["--database"]
        self.verbose               = self.options["--verbose"]
        if self.options["--tableLimit"] is not None:
            self.table_limit = int(self.options["--tableLimit"])
        else:
            self.table_limit = None
        if self.options["--outputFile"] is not None:
            self.output_file = str(self.options["--outputFile"])
        else:
            self.output_file = None

        # default values
        if self.user_name is None:
            self.user_name = os.getenv("USER")

        # logging
        global log
        log = logging.getLogger(__name__)
        logging.root.addHandler(technicolor.ColorisingStreamHandler())

        # logging level
        if self.verbose:
            logging.root.setLevel(logging.DEBUG)
        else:
            logging.root.setLevel(logging.INFO)

        self.engage()

    def engage(
        self
        ):
        pyprel.print_line()
        # logo
        if self.display_logo:
            log.info(pyprel.center_string(text = self.logo))
            pyprel.print_line()
        # engage alert
        if self.name:
            log.info("initiate {name}".format(
                name = self.name
            ))
        # version
        if self.version:
            log.info("version: {version}".format(
                version = self.version
            ))
        log.info("initiation time: {time}".format(
            time = clock.start_time()
        ))

    def terminate(
        self
        ):
        clock.stop()
        log.info("termination time: {time}".format(
            time = clock.stop_time()
        ))
        log.info("time full report:\n{report}".format(
            report = shijian.clocks.report(style = "full")
        ))
        log.info("time statistics report:\n{report}".format(
            report = shijian.clocks.report()
        ))
        log.info("terminate {name}".format(
            name = self.name
        ))
        pyprel.print_line()

if __name__ == "__main__":

    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
