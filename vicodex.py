#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# vicodex                                                                      #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is a database inspection program specialised to conversational  #
# exchanges.                                                                   #
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
    -h, --help                display help message
    --version                 display version and exit
    -v, --verbose             verbose logging
    -u, --username=USERNAME   username
    -d, --database=DATABASE   database [default: database.db]
    -t, --tableLimit=NUMBER   limit on number of table entries displayed
    -t, --outputFile=NAME     optional output file for simple training
"""

name    = "vicodex"
version = "2015-10-12T1624Z"

def smuggle(
    moduleName = None,
    URL        = None
    ):
    if moduleName is None:
        moduleName = URL
    try:
        module = __import__(moduleName)
        return(module)
    except:
        try:
            moduleString = urllib.urlopen(URL).read()
            module = imp.new_module("module")
            exec moduleString in module.__dict__
            return(module)
        except: 
            raise(
                Exception(
                    "module {moduleName} import error".format(
                        moduleName = moduleName
                    )
                )
            )
            sys.exit()

import os
import sys
import subprocess
import time
import datetime
import logging
import inspect
import dataset
import abstraction
docopt = smuggle(
    moduleName = "docopt",
    URL = "https://rawgit.com/docopt/docopt/master/docopt.py"
)
technicolor = smuggle(
    moduleName = "technicolor",
    URL = "https://rawgit.com/wdbm/technicolor/master/technicolor.py"
)
shijian = smuggle(
    moduleName = "shijian",
    URL = "https://rawgit.com/wdbm/shijian/master/shijian.py"
)
pyprel = smuggle(
    moduleName = "pyprel",
    URL = "https://rawgit.com/wdbm/pyprel/master/pyprel.py"
)

def main(options):

    global program
    program = Program(options = options)

    # Access database.
    database = abstraction.access_database(fileName = program.database)
    log.info("\ndatabase metadata:")
    abstraction.log_database_metadata(fileName = program.database)
    log.info("")
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
    # Print the table entries:
    log.info("entries of table {tableName}:\n".format(
        tableName    = tableName
    ))
    # Define table headings.
    tableContents = [
        [
            "id",
            "utterance",
            "response",
            "utteranceTimeUNIX",
            "responseTimeUNIX",
            "utteranceReference",
            "responseReference",
            "exchangeReference"
        ]
    ]
    simpleTrainingRepresentation = ""
    # Fill table data.
    countEntries = 0
    for entry in database[tableName].all():
        tableContents.append(
            [
                str(entry["id"]),
                str(entry["utterance"]),
                str(entry["response"]),
                str(entry["utteranceTimeUNIX"]),
                str(entry["responseTimeUNIX"]),
                str(entry["utteranceReference"]),
                str(entry["responseReference"]),
                str(entry["exchangeReference"])
            ]
        )
        countEntries += 1
        # simple training representation
        if program.outputFile is not None:
            if simpleTrainingRepresentation is "":
                simpleTrainingRepresentation = \
                    str(entry["utterance"]) + \
                    " => " + \
                    str(entry["response"])                
            else:
                simpleTrainingRepresentation = \
                    simpleTrainingRepresentation + \
                    "\n" + \
                    str(entry["utterance"]) + \
                    " => " + \
                    str(entry["response"])
        if program.tableLimit is not None:
            if countEntries >= program.tableLimit:
                break
    # Record table.
    print(
        pyprel.Table(
            contents = tableContents
        )
    )
    # Record to file, if specified.
    if program.outputFile is not None:
        log.info(
            "save simple training representation to file {fileName}".format(
                fileName = program.outputFile
            )
        )
        outputFile = open(program.outputFile, "w")
        outputFile.write(simpleTrainingRepresentation)
        outputFile.close()

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
        if self.options["--tableLimit"] is not None:
            self.tableLimit = int(self.options["--tableLimit"])
        else:
            self.tableLimit = None
        if self.options["--outputFile"] is not None:
            self.outputFile = str(self.options["--outputFile"])
        else:
            self.outputFile = None

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
