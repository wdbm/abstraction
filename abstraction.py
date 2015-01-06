################################################################################
#                                                                              #
# abstraction                                                                  #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program provides data analysis, data selection, data collation and      #
# database utilities for project abstraction.                                  #
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

version = "2015-01-06T1509Z"

import os
import sys
import subprocess
import time
import datetime
import logging
import inspect
import pyprel
import shijian
import dataset
import praw

log = logging.getLogger(__name__)

def access_database(
    database = "database.db"
    ):
    # Access the database.
    log.debug("access database \"{database}\"".format(
        database = database
    ))
    database = dataset.connect("sqlite:///" + database)
    return(database)

def save_database_metadata(
    database = "database.db"
    ):
    database = access_database(database = database)
    # Access or create the exchanges table, delete it and then recreate it.
    tableMetadata = database["metadata"]
    tableMetadata.drop()
    tableMetadata = database["metadata"]
    # Create database metadata.
    log.debug("create database metadata")
    currentTime = shijian.time_UTC()
    metadata = dict(
        name                 = "abstraction",
        description          = "project abstraction conversation "
                               "utterance-response data",
        version              = currentTime,
        lastModificationTime = currentTime
    )
    log.debug(pyprel.dictionaryString(dictionary = metadata))
    # Save metadata to database.
    log.debug("save database metadata")
    tableMetadata.insert(metadata)

def database_metadata(
    database = "database.db"
    ):
    database = access_database(database = database)
    # Access the database metadata.
    log.debug("access database metadata")
    # Check if metadata exists for the database.
    if "metadata" in database.tables:
        for entry in database["metadata"].all():
            metadata = {
                "name":                 entry["name"],
                "description":          entry["description"],
                "version":              entry["version"],
                "lastModificationTime": entry["lastModificationTime"]
            }
    else:
        log.error("database metadata not found")
        raise(Exception)
    return(metadata)

def log_database_metadata(
    database = "database.db"
    ):
    metadata = database_metadata(database = database)
    log.info(pyprel.dictionaryString(dictionary = metadata))
