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
version = "2016-01-12T2238Z"

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
    database = abstraction.access_database(filename = program.database)
    log.info("database metadata:")
    abstraction.log_database_metadata(filename = program.database)
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

        # logging level
        if self.verbose:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)

        self.engage()

    def engage(
        self
        ):
        pyprel.print_line()
        # logo
        if self.display_logo:
            log.info(pyprel.centerString(text = self.logo))
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
