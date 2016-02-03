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
    -h, --help               Show this help message.
    --version                Show the version and exit.
    -v, --verbose            Show verbose logging.
    -s, --silent             silent
    -u, --username=USERNAME  username
    --expression=TEXT        text expression to convert to word vector
                             [default: All those moments will be lost in time.]
    --wordvectormodel=NAME   word vector model
                             [default: Brown_corpus.wvm]
"""

name    = "toywv-1"
version = "2016-02-03T1428Z"
logo    = None

import os
import sys
import subprocess
import time
import datetime
import logging
import technicolor
import inspect
import docopt
import propyte
import pyprel
import shijian
import dataset
import abstraction
from gensim.models import Word2Vec
import numpy

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
    expression        = options["--expression"]
    word_vector_model = options["--wordvectormodel"]

    model_word2vec = abstraction.load_word_vector_model(
        filename = word_vector_model
    )

    # Convert the expression to a word vector.
    expression_word_vector =\
        abstraction.convert_sentence_string_to_word_vector(
            sentence_string = expression,
            model_word2vec  = model_word2vec
        )
    log.info(
        "word vector representation of expression \"{expression}\":"
        "\n{expression_word_vector}".format(
            expression             = expression,
            expression_word_vector = expression_word_vector
        )
    )

    log.info("")

    log.info(
        "word vector representation of expression \"{expression}\" as NumPy "
        "array:\n{expression_NumPy_array}".format(
            expression             = expression,
            expression_NumPy_array = numpy.array_repr(expression_word_vector)
        )
    )

    program.terminate()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
