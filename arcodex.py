#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# arcodex: archive collated exchanges                                          #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is a data collation and archiving program specialised to        #
# conversational exchanges.                                                    #
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
    -h, --help                    Show this help message.
    --version                     Show the version and exit.
    -v, --verbose                 Show verbose logging.
    -r, --subreddits=SUBREDDITS   subreddits [default: changemyview]
    -n, --numberOfUtterances=N    number of utterances to access [default: 10]
    -d, --database=DATABASE       database [default: database.db]
"""

programName    = "arcodex"
programVersion = "2014-10-20T1727Z"

import os
import sys
import time
import logging
from   docopt import docopt
import dataset
import praw as praw
import technicolor as technicolor

def main(options):

    global program
    program = Program(options = options)

    logger.info("accessing exchanges")
    exchangesReddit = access_exchanges_Reddit()
    logger.info("saving exchanges to database")
    save_exchanges_to_database(exchangesReddit)

    logger.info("terminating {programName}".format(
        programName = program.name
    ))

class Exchange(object):

    def __init__(
        self,
        utterance               = None,
        response                = None,
        utteranceTimeUNIX       = None,
        responseTimeUNIX        = None,
        utteranceReference      = None,
        responseReference       = None,
        exchangeReference       = None
        ):
        self.utterance          = utterance
        self.response           = response
        self.utteranceTimeUNIX  = utteranceTimeUNIX
        self.responseTimeUNIX   = responseTimeUNIX
        self.utteranceReference = utteranceReference
        self.responseReference  = responseReference
        self.exchangeReference  = exchangeReference

def access_exchanges_Reddit():
    # Access Reddit.
    logger.info("accessing Reddit API")
    r = praw.Reddit(user_agent = programName)
    # Access each subreddit.
    logger.info("accessing subreddits {subreddits}".format(
        subreddits = program.subreddits
    ))
    for subreddit in program.subreddits:
        logger.info("accessing subreddit \"{subreddit}\"".format(
            subreddit = subreddit
        ))
        submissions = r.get_subreddit(
            subreddit
        ).get_top(
            limit = int(program.numberOfUtterances)
        )
        # Access each submission, its title and its top comment.
        exchanges = []
        for submission in submissions:
            # Access the submission title.
            submissionTitle = submission.title.encode(
                "ascii",
                "ignore"
            )
            # Access the submission URL.
            submissionURL = submission.permalink.encode(
                "ascii",
                "ignore"
            )
            # Access the submission time.
            submissionTimeUNIX = str(submission.created_utc).encode(
                "ascii",
                "ignore"
            )
            logger.debug(
                "accessing submission \"{submissionTitle}\"".format(
                subreddit = subreddit,
                submissionTitle = submissionTitle
            ))
            comments = praw.helpers.flatten_tree(submission.comments)
            if comments:
                # Access the submission top comment.
                commentTopText = comments[0].body.encode(
                    "ascii",
                    "ignore"
                )
                # Access the submission top comment URL.
                commentTopURL = comments[0].permalink.encode(
                    "ascii",
                    "ignore"
                )
                # Access the submission top comment time.
                commentTopTimeUNIX = str(comments[0].created_utc).encode(
                    "ascii",
                    "ignore"
                )
            # Create a new exchange object for the current exchange data and
            # append it to the list of exchanges.
            exchange = Exchange(
                utterance          = submissionTitle,
                response           = commentTopText,
                utteranceTimeUNIX  = submissionTimeUNIX,
                responseTimeUNIX   = commentTopTimeUNIX,
                utteranceReference = submissionURL,
                responseReference  = commentTopURL,
                exchangeReference  = subreddit
            )
            exchanges.append(exchange)
    return(exchanges)

def create_database(
    fileName = None
    ):
    os.system(
        "sqlite3 " + \
        fileName + \
        " \"create table aTable(field1 int); drop table aTable;\""
    )

def save_exchanges_to_database(
    exchanges = None
    ):
    # Check for the database. If it does not exist, create it.
    if not os.path.isfile(program.database):
        logger.info("database {database} nonexistent".format(
            database = program.database
        ))
        logger.info("creating database {database}".format(
            database = program.database
        ))
        create_database(fileName = program.database)
    # Access the database.
    logger.info("accessing database {database}".format(
        database = program.database
    ))
    database = dataset.connect("sqlite:///" + program.database)
    # Access or create the exchanges table.
    tableExchanges = database["exchanges"]
    # Access each exchange and save it to the database.
    for exchange in exchanges:
        tableExchanges.insert(dict(
            utterance          = exchange.utterance,
            response           = exchange.response,
            utteranceTimeUNIX  = exchange.utteranceTimeUNIX,
            responseTimeUNIX   = exchange.responseTimeUNIX,
            utteranceReference = exchange.utteranceReference,
            responseReference  = exchange.responseReference,
            exchangeReference  = exchange.exchangeReference
        ))

class Program(object):

    def __init__(
        self,
        parent  = None,
        options = None
        ):

        # name
        self.name               = programName

        # options
        self.options            = options
        self.subreddits         = self.options["--subreddits"]
        self.numberOfUtterances = self.options["--numberOfUtterances"]
        self.database           = self.options["--database"]
        if "--verbose" in options:
            self.verbose        = True
        else:
            self.verbose        = False

        # default values
        # Create a list of subreddits from the comma-delimited list of
        # subreddits.
        self.subreddits = self.subreddits.split(",")

        ## standard logging
        #global logger
        #logger = logging.getLogger(__name__)
        ##logger = logging.getLogger()
        #logging.basicConfig()

        # technicolor logging
        global logger
        logger = logging.getLogger(__name__)
        #logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(technicolor.ColorisingStreamHandler())

        # logging level
        if self.verbose:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        # run alert
        logger.info("running {name}".format(name = self.name))

if __name__ == "__main__":

    options = docopt(__doc__)
    if options["--version"]:
        print(programVersion)
        exit()
    main(options)
