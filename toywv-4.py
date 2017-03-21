#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# toywv-4                                                                      #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This toy program converts a specified text expression to a word vector. It   #
# also converts a bank of text expressions to word vectors. It compares the    #
# specified text expression word vector to the bank of text expressions word   #
# vectors and returns the closest match.                                       #
#                                                                              #
# copyright (C) 2017 William Breaden Madden                                    #
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

name    = "toywv-4"
version = "2017-03-15T1527Z"
logo    = None

import datetime
import docopt
import inspect
import logging
import numpy
import os
import subprocess
import sys
import time

import abstraction
import dataset
import datavision
from gensim.models import Word2Vec
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

    expression        = options["--expression"]
    word_vector_model = options["--wordvectormodel"]

    model_word2vec = abstraction.load_word_vector_model(
        filename = word_vector_model
    )

    sentences = [
        "What are you dirty hooers doing on my planet?",
        "What time is it?",
        "What can you do?",
        "Change the color from red to black.",
        "All those moments will be lost in time.",
        "All of those moments will be lost in time.",
        "All of those moments are to be lost in time."
    ]

    result = most_similar_expression(
        expression     = expression,
        expressions    = sentences,
        model_word2vec = model_word2vec
    )

    pyprel.print_line()
    log.info("input expression:        {expression}".format(
        expression = expression
    ))
    log.info("most similar expression: {expression}".format(
        expression = result
    ))
    pyprel.print_line()

    program.terminate()

def most_similar_expression(
    expression     = None,
    expressions    = None,
    model_word2vec = None,
    detail         = True
    ):

    working_expression_NL = expression

    # Convert the expression to a word vector.
    working_expression_WV =\
        abstraction.convert_sentence_string_to_word_vector(
            sentence_string = working_expression_NL,
            model_word2vec  = model_word2vec
        )

    stored_expressions = dict()
    for expression in expressions:
        stored_expressions[expression] =\
            abstraction.convert_sentence_string_to_word_vector(
                sentence_string = expression,
                model_word2vec  = model_word2vec
            )

    # Define table headings.
    table_contents = [[
        "working expression natural language",
        "stored expression natural language",
        "absolute magnitude difference between working amd stored expression "
        "word vectors",
        "angle between working and stored expression word vectors"
    ]]

    # Compare the expression word vector representation to existing word
    # vectors.
    magnitude_differences      = []
    angles                     = []
    stored_expressions_NL_list = []
    magnitude_working_expression_WV = datavision.magnitude(working_expression_WV)
    for stored_expression_NL in stored_expressions:
        stored_expression_WV = stored_expressions[stored_expression_NL]
        magnitude_stored_expression_WV = datavision.magnitude(stored_expression_WV)
        magnitude_difference_working_expression_WV_stored_expression_WV = abs(
            magnitude_working_expression_WV - magnitude_stored_expression_WV
        )
        angle_working_expression_WV_stored_expression_WV = datavision.angle(
            working_expression_WV,
            stored_expression_WV
        )
        # Store comparison results in lists.
        magnitude_differences.append(
            magnitude_difference_working_expression_WV_stored_expression_WV
        )
        angles.append(
            angle_working_expression_WV_stored_expression_WV
        )
        stored_expressions_NL_list.append(
            stored_expression_NL
        )
        # Build table.
        table_contents.append([
            str(working_expression_NL),
            str(stored_expression_NL),
            str(magnitude_difference_working_expression_WV_stored_expression_WV),
            str(angle_working_expression_WV_stored_expression_WV)]
        )

    if detail:
        # Record table.
        print(
            pyprel.Table(
                contents = table_contents
            )
        )

    index_minimum_angles = angles.index(min(angles))
    translation_expression_NL = stored_expressions_NL_list[index_minimum_angles]

    return translation_expression_NL

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
