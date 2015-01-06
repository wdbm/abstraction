#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# reducodex                                                                    #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program inspects an existing database of conversational exchanges,      #
# removes duplicate entries, creates simplified identifiers for entries and    #
# then writes a new database of these entries.                                 #
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
    -h, --help                      Show this help message.
    --version                       Show the version and exit.
    -v, --verbose                   Show verbose logging.
    -u, --username=USERNAME         username
    -d, --inputdatabase=DATABASE    database [default: database.db]
    -d, --outputdatabase=DATABASE   database [default: database_1.db]
"""

name    = "reducodex"
version = "2015-01-06T1056Z"

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

def main(options):

    global program
    program = Program(options = options)

    # Access database.
    log.info("access database \"{database}\"".format(
        database = program.database
    ))
    database = dataset.connect("sqlite:///" + program.database)
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
    # Build a list of unique exchanges.
    exchanges = []
    for entry in database[tableName].all():
        # Create a new exchange object for the existing exchange data, check its
        # utterance data against existing utterance data in the new list of
        # exchanges and append it to the new list of exchanges if it does not
        # exist in the list.
        exchange = Exchange(
            utterance          = entry["utterance"],
            response           = entry["response"],
            utteranceTimeUNIX  = entry["utteranceTimeUNIX"],
            responseTimeUNIX   = entry["responseTimeUNIX"],
            utteranceReference = entry["utteranceReference"],
            responseReference  = entry["responseReference"],
            exchangeReference  = entry["exchangeReference"]
        )
        # Check new exchange against exchanges in new list.
        appendFlag = True
        for exchangeInNewList in exchanges:
            if exchange.utterance == exchangeInNewList.utterance:
                appendFlag = False
        if appendFlag is True:
            log.debug("keep exchange \"{utterance}\"".format(
                utterance = exchange.utterance
            ))
            exchanges.append(exchange)
        else:
            log.debug("skip exchange \"{utterance}\"".format(
                utterance = exchange.utterance
            ))

    log.info("save exchanges to database (only those not saved previously)")
    save_exchanges_to_database(
        exchanges = exchanges,
        database  = program.databaseOut
    )

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

def create_database(
    fileName = None
    ):
    os.system(
        "sqlite3 " + \
        fileName + \
        " \"create table aTable(field1 int); drop table aTable;\""
    )

def save_exchanges_to_database(
    exchanges = None,
    database  = "database.db"
    ):
    # Check for the database. If it does not exist, create it.
    if not os.path.isfile(database):
        log.info("database {database} nonexistent".format(
            database = database
        ))
        log.info("create database {database}".format(
            database = database
        ))
        create_database(fileName = database)
    # Access the database.
    log.info("access database {database}".format(
        database = database
    ))
    database = dataset.connect("sqlite:///" + database)
    # Access or create the exchanges table.
    tableExchanges = database["exchanges"]
    # Access each exchange. Check the database for the utterance of the
    # exchange. If the utterance of the exchange is not in the database, save
    # the exchange to the database.
    for exchange in exchanges:
        if database["exchanges"].find_one(
                utterance = exchange.utterance
            ) is None:
            log.debug("save exchange \"{utterance}\"".format(
                utterance = exchange.utterance
            ))
            tableExchanges.insert(dict(
                utterance          = exchange.utterance,
                response           = exchange.response,
                utteranceTimeUNIX  = exchange.utteranceTimeUNIX,
                responseTimeUNIX   = exchange.responseTimeUNIX,
                utteranceReference = exchange.utteranceReference,
                responseReference  = exchange.responseReference,
                exchangeReference  = exchange.exchangeReference
            ))
        else:
            log.debug("skip previously-saved exchange \"{utterance}\"".format(
                utterance = exchange.utterance
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
        self.database              = self.options["--inputdatabase"]
        self.databaseOut           = self.options["--outputdatabase"]
        if "--verbose" in options:
            self.verbose           = True
        else:
            self.verbose           = False

        # default values
        if self.userName is None:
            self.userName = os.getenv("USER")
        self.databaseOut = shijian.proposeFileName(fileName = self.databaseOut)

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
