#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# vecodex                                                                      #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This development version program converts string representations of          #
# exchanges in an existing database of conversational exchanges to word vector #
# representations.                                                             #
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
    -h, --help               Show this help message.
    --version                Show the version and exit.
    -v, --verbose            Show verbose logging.
    -s, --silent             silent
    -u, --username=USERNAME  username
    -d, --database=DATABASE  database [default: database.db]
"""

name    = "vecodex"
version = "2016-03-28T1755Z"
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
    database = options["--database"]

    model_word2vec = abstraction.model_word2vec_Brown_Corpus()

    # Access database.
    database = abstraction.access_database(filename = database)
    log.info("database metadata:")
    abstraction.log_database_metadata(filename = database)
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
    log.info(
        "create word vector representations of each utterance and response " +
        "of all exchanges"
    )
    # Create a vector representation of each utterance and response of all
    # exchanges.
    for entry in database[table_name].all():
        utterance = entry["utterance"]
        utterance_word_vector =\
            abstraction.convert_sentence_string_to_word_vector(
                sentence_string = utterance,
                model_word2vec  = model_word2vec
            )
        log.info(
            "word vector representation of utterance \"{utterance}\":"
            "\n{utterance_word_vector}".format(
                utterance             = utterance,
                utterance_word_vector = utterance_word_vector
            )
        )
        response = entry["response"]
        response_word_vector =\
            abstraction.convert_sentence_string_to_word_vector(
                sentence_string = response,
                model_word2vec  = model_word2vec
            )
        log.info(
            "word vector representation of response \"{response}\":"
            "\n{response_word_vector}".format(
                response             = response,
                response_word_vector = response_word_vector
            )
        )

    program.terminate()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
