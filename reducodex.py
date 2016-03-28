#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# reducodex                                                                    #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program inspects an existing database of conversational exchanges,      #
# removes duplicate entries, creates simplified identifiers for entries and    #
# then writes a new database of these entries.                                 #
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
    -h, --help                 Show this help message.
    --version                  Show the version and exit.
    -v, --verbose              Show verbose logging.
    -s, --silent               silent
    -u, --username=USERNAME    username
    -d, --inputdatabase=FILE   database [default: database.db]
    -d, --outputdatabase=FILE  database [default: database_1.db]
"""

name    = "reducodex"
version = "2016-03-28T1804Z"
logo    = None

import datetime
import docopt
import inspect
import logging
import os
import subprocess
import sys
import time

import abstraction
import dataset
import propyte
import pyprel
import shijian
import technicolor

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
    database     = options["--inputdatabase"]
    database_out = options["--outputdatabase"]

    # Access database.
    database = abstraction.access_database(filename = database)
    log.info("database metadata:")
    abstraction.log_database_metadata(filename = database)
    # Print the tables in the database.
    log.info("tables in database: {tables}".format(
        tables = database.tables
    ))
    # Access the exchanges table.
    tablename = "exchanges"
    log.info("access table \"{tablename}\"".format(
        tablename = tablename
    ))
    # Print the columns of the table.
    log.info("columns in table \"{tablename}\": {columns}".format(
        tablename = tablename,
        columns   = database[tablename].columns
    ))
    # Print the number of rows of the table.
    log.info("number of rows in table \"{tablename}\": {number_of_rows}".format(
        tablename      = tablename,
        number_of_rows = str(len(database[tablename]))
    ))
    # Build a list of unique exchanges.
    exchanges = []
    for entry in database[tablename].all():
        # Create a new exchange object for the existing exchange data, check its
        # utterance data against existing utterance data in the new list of
        # exchanges and append it to the new list of exchanges if it does not
        # exist in the list.
        exchange = abstraction.Exchange(
            utterance           = entry["utterance"],
            response            = entry["response"],
            utterance_time_UNIX = entry["utteranceTimeUNIX"],
            response_time_UNIX  = entry["responseTimeUNIX"],
            utterance_reference = entry["utteranceReference"],
            response_reference  = entry["responseReference"],
            exchange_reference  = entry["exchangeReference"]
        )
        # Check new exchange against exchanges in new list.
        append_flag = True
        for exchange_in_new_list in exchanges:
            if exchange.utterance == exchange_in_new_list.utterance:
                append_flag = False
        if append_flag is True:
            log.debug("keep exchange \"{utterance}\"".format(
                utterance = exchange.utterance
            ))
            exchanges.append(exchange)
        else:
            log.debug("skip exchange \"{utterance}\"".format(
                utterance = exchange.utterance
            ))
    # Save the exchanges to the new database.
    log.info("save exchanges to database (only those not saved previously)")
    abstraction.save_exchanges_to_database(
        exchanges = exchanges,
        filename  = database_out
    )
    # Save metadata to the new database.
    abstraction.save_database_metadata(filename = database_out)

    program.terminate()

if __name__ == "__main__":

    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
