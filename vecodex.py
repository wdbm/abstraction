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
    -h, --help                Show this help message.
    --version                 Show the version and exit.
    -v, --verbose             Show verbose logging.
    -u, --username=USERNAME   username
    -d, --database=DATABASE   database [default: database.db]
"""

name    = "vecodex"
version = "2015-03-31T2150Z"

import os
import sys
import subprocess
import time
import datetime
import logging
import technicolor
import inspect
import docopt
import pyprel
import shijian
import dataset
import abstraction

def main(options):

    global program
    program = Program(options = options)

    model_word2vec = abstraction.model_word2vec_Brown_Corpus()

    # Access database.
    database = abstraction.access_database(fileName = program.database)
    log.info("database metadata:")
    abstraction.log_database_metadata(fileName = program.database)
    # Print the tables in the database.
    log.info("tables in database: {tables}".format(
        tables = database.tables
    ))
    # Access the exchanges table.
    tableName = "exchanges"
    log.info("access table \"{tableName}\"".format(
        tableName = tableName
    ))
    # Print the columns of the table.
    log.info("columns in table \"{tableName}\": {columns}".format(
        tableName = tableName,
        columns   = database[tableName].columns
    ))
    # Print the number of rows of the table.
    log.info("number of rows in table \"{tableName}\": {numberOfRows}".format(
        tableName    = tableName,
        numberOfRows = str(len(database[tableName]))
    ))
    log.info(
        "create word vector representations of each utterance and response " +
        "of all exchanges"
    )
    # Create a vector representation of each utterance and response of all
    # exchanges.
    for entry in database[tableName].all():
        utterance = entry["utterance"]
        utteranceWordVector =\
            abstraction.convert_sentence_string_to_word_vector(
                sentenceString = utterance,
                model_word2vec = model_word2vec
            )
        log.info(
            "word vector representation of utterance \"{utterance}\":"
            "\n{utteranceWordVector}".format(
                utterance           = utterance,
                utteranceWordVector = utteranceWordVector
            )
        )
        response = entry["response"]
        responseWordVector =\
            abstraction.convert_sentence_string_to_word_vector(
                sentenceString = response,
                model_word2vec = model_word2vec
            )
        log.info(
            "word vector representation of response \"{response}\":"
            "\n{responseWordVector}".format(
                response           = response,
                responseWordVector = responseWordVector
            )
        )

    program.terminate()

class Program(object):

    def __init__(
        self,
        parent  = None,
        options = None
        ):

        # internal options
        self.displayLogo           = True

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
            self.logo              = pyprel.renderBanner(
                                         text = self.name.upper()
                                     )
        else:
            self.displayLogo       = False
            self.logo              = None

        # options
        self.options               = options
        self.userName              = self.options["--username"]
        self.database              = self.options["--database"]
        self.verbose               = self.options["--verbose"]

        # default values
        if self.userName is None:
            self.userName = os.getenv("USER")

        # logging
        global log
        log = logging.getLogger(__name__)
        logging.root.addHandler(technicolor.ColorisingStreamHandler())

        # logging level
        if self.verbose:
            logging.root.setLevel(logging.DEBUG)
        else:
            logging.root.setLevel(logging.INFO)

        # logging level
        if self.verbose:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)

        self.engage()

    def engage(
        self
        ):
        pyprel.printLine()
        # logo
        if self.displayLogo:
            log.info(pyprel.centerString(text = self.logo))
            pyprel.printLine()
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
            time = clock.startTime()
        ))

    def terminate(
        self
        ):
        clock.stop()
        log.info("termination time: {time}".format(
            time = clock.stopTime()
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
        pyprel.printLine()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
