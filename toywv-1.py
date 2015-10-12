#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# toywv-1                                                                      #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This toy program converts a specified text expression to a word vector.      #
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

Usage:
    program [options]

Options:
    -h, --help                Show this help message.
    --version                 Show the version and exit.
    -v, --verbose             Show verbose logging.
    -u, --username=USERNAME   username
    --expression=TEXT         text expression to convert to word vector
                              [default: All those moments will be lost in time.]
    --wordvectormodel=NAME    word vector model
                              [default: Brown_corpus.wvm]
"""

name    = "toywv-1"
version = "2015-10-12T2148Z"

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
from gensim.models import Word2Vec
import numpy

def main(options):

    global program
    program = Program(options = options)

    model_word2vec = abstraction.load_word_vector_model(
        fileName = program.wordVectorModel
    )

    # Convert the expression to a word vector.
    expressionWordVector =\
        abstraction.convert_sentence_string_to_word_vector(
            sentenceString = program.expression,
            model_word2vec = model_word2vec
        )
    log.info(
        "word vector representation of expression \"{expression}\":"
        "\n{expressionWordVector}".format(
            expression           = program.expression,
            expressionWordVector = expressionWordVector
        )
    )

    log.info("")

    log.info(
        "word vector representation of expression \"{expression}\" as NumPy "
        "array:\n{expressionNumPyArray}".format(
            expression           = program.expression,
            expressionNumPyArray = numpy.array_repr(expressionWordVector)
        )
    )

    program.terminate()

def ensure_file_existence(fileName):
    log.debug("ensure existence of file {fileName}".format(
        fileName = fileName
    ))
    if not os.path.isfile(os.path.expandvars(fileName)):
        log.error("file {fileName} does not exist".format(
            fileName = fileName
        ))
        program.terminate()
        raise(Exception)
    else:
        log.debug("file {fileName} found".format(
            fileName = fileName
        ))

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
        self.verbose               = self.options["--verbose"]
        self.expression            = self.options["--expression"]
        self.wordVectorModel       = self.options["--wordvectormodel"]

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
