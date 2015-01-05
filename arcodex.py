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
    -u, --username=USERNAME       username
    -r, --subreddits=SUBREDDITS   subreddits [default: changemyview]
    -n, --numberOfUtterances=N    number of utterances to access [default: 10]
    -d, --database=DATABASE       database [default: database.db]
"""

name    = "arcodex"
version = "2015-01-05T1454Z"
#logo = (
#"    ___    ____  __________  ____  _______  __\n"
#"   /   |  / __ \/ ____/ __ \/ __ \/ ____/ |/ /\n"
#"  / /| | / /_/ / /   / / / / / / / __/  |   / \n"
#" / ___ |/ _, _/ /___/ /_/ / /_/ / /___ /   |  \n"
#"/_/  |_/_/ |_|\____/\____/_____/_____//_/|_|  \n"
#"                                              "
#)

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
import praw

def main(options):

    global program
    program = Program(options = options)

    log.info("accessing exchanges")
    exchangesReddit = access_exchanges_Reddit()
    log.info("saving exchanges to database")
    save_exchanges_to_database(exchangesReddit)

    program.terminate()

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
    log.info("accessing Reddit API")
    r = praw.Reddit(user_agent = name)
    # Access each subreddit.
    log.info("accessing subreddits {subreddits}".format(
        subreddits = program.subreddits
    ))
    for subreddit in program.subreddits:
        log.info("accessing subreddit \"{subreddit}\"".format(
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
            log.debug(
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
            # Pause to avoid overtaxing Reddit.
            #time.sleep(2)
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
        log.info("database {database} nonexistent".format(
            database = program.database
        ))
        log.info("creating database {database}".format(
            database = program.database
        ))
        create_database(fileName = program.database)
    # Access the database.
    log.info("accessing database {database}".format(
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
        self.options            = options
        self.userName           = self.options["--username"]
        self.subreddits         = self.options["--subreddits"]
        self.numberOfUtterances = self.options["--numberOfUtterances"]
        self.database           = self.options["--database"]
        if "--verbose" in options:
            self.verbose        = True
        else:
            self.verbose        = False

        # default values
        if self.userName is None:
            self.userName = os.getenv("USER")
        # Create a list of subreddits from the comma-delimited list of
        # subreddits.
        self.subreddits = self.subreddits.split(",")

        ## standard logging
        #global log
        #log = logging.getLogger(__name__)
        ##log = logging.getLogger()
        #logging.basicConfig()

        # technicolor logging
        global log
        log = logging.getLogger(__name__)
        #log = logging.getLogger()
        log.setLevel(logging.DEBUG)
        log.addHandler(technicolor.ColorisingStreamHandler())

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
