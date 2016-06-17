#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# fix_database                                                                 #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program inspects an existing database of conversational exchanges,      #
# changes data stored in the database to appropriate types and then saves the  #
# changed data to a new database. The original database is not modified.       #
#                                                                              #
# copyright (C) 2016 William Breaden Madden                                    #
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
    --inputdatabase=FILE     database       [default: database.db]
    --outputdatabase=FILE    database       [default: database_1.db]
    --table=NAME             table          [default: exchanges]
    --tablemetadata=NAME     metadata table [default: metadata]
"""

name    = "fix_database"
version = "2016-06-17T1559Z"
logo    = None

import ast
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

    filename_database     = options["--inputdatabase"]
    filename_database_out = options["--outputdatabase"]
    name_table            = options["--table"]
    name_table_metadata   = options["--tablemetadata"]

    log.info("\naccess database {filename}".format(
        filename = filename_database
    ))
    database = dataset.connect(
        "sqlite:///{filename_database}".format(
            filename_database = filename_database
        )
    )
    log.info("access table \"{name_table}\"".format(
        name_table = name_table
    ))
    table = database[name_table]
    log.info("number of rows in table \"{name_table}\": {number_of_rows}".format(
        name_table     = name_table,
        number_of_rows = str(len(table))
    ))

    # Fix database with data version 2015-01-06T172242Z.

    # Build a list of unique exchanges.
    exchanges = []
    for entry in table:

        utterance           = entry["utterance"]
        response            = entry["response"]
        utterance_time_UNIX = entry["utteranceTimeUNIX"]
        response_time_UNIX  = entry["responseTimeUNIX"]
        utterance_reference = entry["utteranceReference"]
        response_reference  = entry["responseReference"]
        exchange_reference  = entry["exchangeReference"]

        if type(utterance_reference) is tuple:
            log.debug("\nchange utterance reference")
            log.debug("from:\n{utterance_reference}".format(
                utterance_reference = utterance_reference
            ))
            utterance_reference = utterance_reference[0]
            log.debug("to:\n{utterance_reference}".format(
                utterance_reference = utterance_reference
            ))
        if type(response_reference) is tuple:
            log.debug("\nchange response reference")
            log.debug("from:\n{response_reference}".format(
                response_reference = response_reference
            ))
            response_reference = response_reference[0]
            log.debug("to:\n{response_reference}".format(
                response_reference = response_reference
            ))
        if exchange_reference[0] == "(":
            log.debug("\nchange exchange reference")
            log.debug("from:\n{exchange_reference}".format(
                exchange_reference = exchange_reference
            ))
            exchange_reference = ast.literal_eval(exchange_reference)
            exchange_reference = unicode(str(exchange_reference[0]), "utf-8")
            log.debug("to:\n{exchange_reference}".format(
                exchange_reference = exchange_reference
            ))

        # Create a new exchange object using the fixed entries and append it to
        # the list of modified exchanges.
        exchange = abstraction.Exchange(
            utterance           = utterance,
            response            = response,
            utterance_time_UNIX = utterance_time_UNIX,
            response_time_UNIX  = response_time_UNIX,
            utterance_reference = utterance_reference,
            response_reference  = response_reference,
            exchange_reference  = exchange_reference
        )
        exchange.printout()
        exchanges.append(exchange)
    # Save the exchanges to the new database.
    log.info("save exchanges to database")
    abstraction.save_exchanges_to_database(
        exchanges = exchanges,
        filename  = filename_database_out
    )
    # Save metadata to the new database.
    abstraction.save_database_metadata(filename = filename_database_out)

    program.terminate()

if __name__ == "__main__":

    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
