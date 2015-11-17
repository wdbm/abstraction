#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# vcodex                                                                       #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program converts conversational exchanges to word vector                #
# representations and adds or updates an abstraction database with these       #
# vectors.                                                                     #
#                                                                              #
# 2015 Will Breaden Madden, w.bm@cern.ch                                       #
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
    -d, --database=FILE      database
                             [default: database.db]
    --wordvectormodel=NAME   word vector model
                             [default: Brown_corpus.wvm]
"""

name    = "vcodex"
version = "2015-11-17T1306Z"
logo    = None

import os
import sys
import logging
import docopt
import technicolor
import shijian
import pyprel
import propyte
import abstraction

@shijian.timer
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
    database        = options["--database"]
    wordVectorModel = options["--wordvectormodel"]

    log.info("")

    log.info("load word vector model {model}".format(
        model = wordVectorModel
    ))
    model_word2vec = abstraction.load_word_vector_model(
        fileName = wordVectorModel
    )
    log.info("add exchange word vectors to database {database}".format(
        database = database
    ))
    abstraction.add_exchange_word_vectors_to_database(
        fileName       = database,
        model_word2vec = model_word2vec
    )

    log.info("")

    program.terminate()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
