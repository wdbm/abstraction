################################################################################
#                                                                              #
# abstraction                                                                  #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program provides data analysis, data selection, data collation,         #
# database utilities and word2vec utilities for project abstraction.           #
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
from __future__ import division

version = "2016-06-01T1602Z"

import csv
import datetime
import inspect
import itertools
import logging
import math
import os
import pickle
import re
import sys
import subprocess
import time

import dataset
import datavision
from gensim.models import Word2Vec
import nltk
import matplotlib
import matplotlib.pyplot
import numpy
import praw
import propyte
import pyprel
import skflow
import sklearn
import sklearn.cross_validation
import sklearn.metrics
import shijian
with propyte.import_ganzfeld():
    from ROOT import *

log = logging.getLogger(__name__)

################################################################################
#                                                                              #
# setup                                                                        #
#                                                                              #
################################################################################

@shijian.timer
def setup():
    # Download NLTK data.
    downloader = nltk.downloader.Downloader("http://nltk.github.com/nltk_data/")
    downloader.download("all")

################################################################################
#                                                                              #
# interfaces                                                                   #
#                                                                              #
################################################################################

def generate_response(
    utterance = None,
    style     = "2016-05-20T0902Z"
    ):
    if style == "2016-05-20T0902Z":
        return "hello world"
    else:
        return "hello world"

################################################################################
#                                                                              #
# databases                                                                    #
#                                                                              #
################################################################################

@shijian.timer
def create_database(
    filename = None
    ):
    os.system(
        "sqlite3 " + \
        filename + \
        " \"create table aTable(field1 int); drop table aTable;\""
    )

@shijian.timer
def access_database(
    filename = "database.db"
    ):
    # Access the database.
    log.debug("access database \"{filename}\"".format(
        filename = filename
    ))
    database = dataset.connect("sqlite:///" + str(filename))
    return database

@shijian.timer
def save_database_metadata(
    filename = "database.db"
    ):
    database = access_database(filename = filename)
    # Access or create the metadata table, delete it and then recreate it.
    table_metadata = database["metadata"]
    table_metadata.drop()
    table_metadata = database["metadata"]
    # Create database metadata.
    log.debug("create database metadata")
    current_time = shijian.time_UTC()
    metadata = dict(
        name                   = "abstraction",
        description            = "project abstraction conversation "
                                 "utterance-response data",
        version                = "2015-01-06T172242Z",
        last_modification_time = current_time
    )
    log.debug("database metadata:")
    log.debug(pyprel.dictionary_string(dictionary = metadata))
    # Save metadata to database.
    log.debug("save database metadata")
    table_metadata.insert(metadata)

@shijian.timer
def database_metadata(
    filename = "database.db"
    ):
    database = access_database(filename = filename)
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
        program.terminate()
        raise Exception
    return metadata

@shijian.timer
def log_database_metadata(
    filename = "database.db"
    ):
    metadata = database_metadata(filename = filename)
    log.info(pyprel.dictionary_string(dictionary = metadata))

@shijian.timer
def add_exchange_word_vectors_to_database(
    filename       = "database.db",
    model_word2vec = None
    ):
    # Ensure that the database exists.
    if not os.path.isfile(filename):
        log.info("database {filename} nonexistent".format(
            filename = filename
        ))
        program.terminate()
        raise Exception
    # Access the database.
    database = access_database(filename = filename)
    # Access or create the exchanges table.
    table_exchanges = database["exchanges"]
    # Access exchanges.
    table_name = "exchanges"
    # progress
    progress = shijian.Progress()
    progress.engage_quick_calculation_mode()
    number_of_entries = len(database[table_name])
    for entry_index, entry in enumerate(database[table_name].all()):
        unique_identifier = str(entry["id"])
        # Create word vector representations of utterances and responses and
        # add them or update them in the database.
        try:
            utterance_word_vector_NumPy_array = numpy.array_repr(
                convert_sentence_string_to_word_vector(
                    sentence_string = str(entry["utterance"]),
                    model_word2vec  = model_word2vec
                )
            )
            response_word_vector_NumPy_array = numpy.array_repr(
                convert_sentence_string_to_word_vector(
                    sentence_string = str(entry["response"]),
                    model_word2vec  = model_word2vec
                )
            )
            data = dict(
                id                  = unique_identifier,
                utteranceWordVector = utterance_word_vector_NumPy_array,
                responseWordVector  = response_word_vector_NumPy_array
            )
        except:
            data = dict(
                id                  = unique_identifier,
                utteranceWordVector = None,
                responseWordVector  = None
            )
        database[table_name].update(data, ["id"])
        print progress.add_datum(fraction = entry_index / number_of_entries),

@shijian.timer
def load_exchange_word_vectors(
    filename                 = "database.db",
    maximum_number_of_events = None
    ):
    """
    Load exchange data and return dataset.
    """
    log.info("load word vectors of database {filename}".format(
        filename = filename
    ))
    # Ensure that the database exists.
    if not os.path.isfile(filename):
        log.info("database {filename} nonexistent".format(
            filename = filename
        ))
        program.terminate()
        raise Exception
    # Access the database.
    database = access_database(filename = filename)
    # Access or create the exchanges table.
    table_exchanges = database["exchanges"]
    # Access exchanges.
    table_name = "exchanges"
    # Create a datavision dataset.
    data = datavision.Dataset()
    # progress
    progress = shijian.Progress()
    progress.engage_quick_calculation_mode()
    number_of_entries = len(database[table_name])
    index = 0
    for index_entry, entry in enumerate(database[table_name].all()):
        if maximum_number_of_events is not None and\
            index >= int(maximum_number_of_events):
            log.info(
                "loaded maximum requested number of events " +
                "({maximum_number_of_events})\r".format(
                    maximum_number_of_events = maximum_number_of_events
                )
            )
            break
        #unique_identifier = str(entry["id"])
        utteranceWordVector = str(entry["utteranceWordVector"])
        responseWordVector = str(entry["responseWordVector"])
        if utteranceWordVector != "None" and responseWordVector != "None":
            index += 1

            utteranceWordVector = eval("numpy." + utteranceWordVector.replace("float32", "numpy.float32"))
            responseWordVector  = eval("numpy." + responseWordVector.replace("float32", "numpy.float32"))
            data.variable(index = index, name = "utteranceWordVector", value = utteranceWordVector)
            data.variable(index = index, name = "responseWordVector",  value = responseWordVector )

            #utteranceWordVector = list(eval("numpy." + utteranceWordVector.replace("float32", "numpy.float32")))
            #responseWordVector  = list(eval("numpy." + responseWordVector.replace("float32", "numpy.float32")))
            #for index_component, component in enumerate(utteranceWordVector):
            #    data.variable(index = index, name = "uwv" + str(index_component), value = component)
            #for index_component, component in enumerate(responseWordVector):
            #    data.variable(index = index, name = "rwv" + str(index_component), value = component)

        print progress.add_datum(fraction = index_entry / number_of_entries),
    return data

################################################################################
#                                                                              #
# physics data                                                                 #
#                                                                              #
################################################################################

@shijian.timer
def open_ROOT_file(
    filename,
    ):
    ensure_file_existence(filename)
    log.info("access file {filename}".format(
        filename = filename
    ))
    return TFile.Open(filename)

@shijian.timer
def access_SUSY_dataset_format_file(filename):
    """
    This function accesses a CSV file containing data of the form of the [SUSY
    dataset](https://archive.ics.uci.edu/ml/datasets/SUSY), i.e. with the first
    column being class labels and other columns being features.
    """
    # Load the CSV file to a list.
    with open(filename, "rb") as dataset_file:
        dataset_CSV = [row for row in csv.reader(dataset_file, delimiter = ",")]
        # Reorganise the data.
        return [
            i for i in itertools.chain(*[list((element[1:],
            [int(float(element[0]))])) for element in dataset_CSV])
        ]

@shijian.timer
def load_HEP_data(
    ROOT_filename            = "output.root",
    tree_name                = "nominal",
    maximum_number_of_events = None
    ):
    """
    Load HEP data and return dataset.
    """
    ROOT_file        = open_ROOT_file(ROOT_filename)
    tree             = ROOT_file.Get(tree_name)
    number_of_events = tree.GetEntries()
    data             = datavision.Dataset()

    progress = shijian.Progress()
    progress.engage_quick_calculation_mode()
    # counters
    number_of_events_loaded = 0

    log.info("")

    index = 0
    for event in tree:

        if maximum_number_of_events is not None and\
            number_of_events_loaded >= int(maximum_number_of_events):
            log.info(
                "loaded maximum requested number of events " +
                "({maximum_number_of_events})\r".format(
                    maximum_number_of_events = maximum_number_of_events
                )
            )
            break
        print progress.add_datum(fraction = (index + 2) / number_of_events),
    
        if select_event(event):
            index += 1
            #event.GetReadEntry()
            #data.variable(index = index, name = "eventNumber",        value = event.eventNumber)
            data.variable(index = index, name = "el_1_pt",            value = event.el_pt[0])
            #data.variable(index = index, name = "el_1_eta",           value = event.el_eta[0])
            #data.variable(index = index, name = "el_1_phi",           value = event.el_phi[0])
            ##data.variable(index = index, name = "jet_1_pt",           value = event.jet_pt[0])
            #data.variable(index = index, name = "jet_1_eta",          value = event.jet_eta[0])
            #data.variable(index = index, name = "jet_1_phi",          value = event.jet_phi[0])
            ##data.variable(index = index, name = "jet_1_e",            value = event.jet_e[0])
            ##data.variable(index = index, name = "jet_2_pt",           value = event.jet_pt[1])
            #data.variable(index = index, name = "jet_2_eta",          value = event.jet_eta[1])
            #data.variable(index = index, name = "jet_2_phi",          value = event.jet_phi[1])
            ##data.variable(index = index, name = "jet_2_e",            value = event.jet_e[1])
            #data.variable(index = index, name = "nJets",              value = event.nJets)
            ##data.variable(index = index, name = "nBTags",             value = event.nBTags)
            ##data.variable(index = index, name = "nLjets",             value = event.nLjets)
            ##data.variable(index = index, name = "ljet_1_m",           value = event.ljet_m[0])
            #data.variable(index = index, name = "met",                value = event.met_met)
            #data.variable(index = index, name = "met_phi",            value = event.met_phi)
            #data.variable(index = index, name = "Centrality_all",     value = event.Centrality_all)
            #data.variable(index = index, name = "Mbb_MindR",          value = event.Mbb_MindR)
            #data.variable(index = index, name = "ljet_tau21",         value = event.ljet_tau21),
            #data.variable(index = index, name = "ljet_tau32",         value = event.ljet_tau32),
            #data.variable(index = index, name = "Aplan_bjets",        value = event.Aplan_bjets),
            #data.variable(index = index, name = "H4_all",             value = event.H4_all),
            #data.variable(index = index, name = "NBFricoNN_6jin4bin", value = event.NBFricoNN_6jin4bin),
            #data.variable(index = index, name = "NBFricoNN_6jin3bex", value = event.NBFricoNN_6jin3bex),
            #data.variable(index = index, name = "NBFricoNN_5jex4bin", value = event.NBFricoNN_5jex4bin),
            #data.variable(index = index, name = "NBFricoNN_3jex3bex", value = event.NBFricoNN_3jex3bex),
            #data.variable(index = index, name = "NBFricoNN_4jin3bex", value = event.NBFricoNN_4jin3bex),
            #data.variable(index = index, name = "NBFricoNN_4jin4bin", value = event.NBFricoNN_4jin4bin)

            number_of_events_loaded += 1

    log.info("")

    return data

@shijian.timer
def load_sklearn_dataset_to_datavision_dataset(
    sklearn_dataset = None
    ):
    data = datavision.Dataset()

    # Define variable names.
    if not hasattr(sklearn_dataset, "feature_names"):
        feature_names = ["feature_" + str(count) for count in range(0, len(sklearn_dataset.data[0]))]
    else:
        feature_names = sklearn_dataset.feature_names
    if not hasattr(sklearn_dataset, "target_names"):
        target_names = "target"
    else:
        target_names = sklearn_dataset.target_names

    for index_entry, (features_entry, targets_entry) in enumerate(zip(
        sklearn_dataset.data,
        sklearn_dataset.target
    )):
        for index_variable, variable_name in enumerate(feature_names):
            data.variable(index = index_entry, name = variable_name, value = sklearn_dataset.data[index_entry][index_variable])
        data.variable(index = index_entry, name = target_names, value = sklearn_dataset.target[index_entry])
    return data

@shijian.timer
def load_sklearn_dataset_to_abstraction_dataset(
    sklearn_dataset = None
    ):
    _data = []
    for features_entry, targets_entry in zip(
        sklearn_dataset.data,
        sklearn_dataset.target
    ):
        _data.extend([features_entry])
        _data.extend([targets_entry])
    dataset = Dataset(data = _data)
    return dataset

@shijian.timer
def convert_HEP_datasets_from_datavision_datasets_to_abstraction_datasets(
    datasets    = None, # a single dataset or a list of datasets
    apply_class = True
    ):
    # If one dataset is specified, contain it in a list.
    if not isinstance(datasets, list):
        datasets = [datasets]
    _data = []
    for dataset in datasets:
        for index in dataset.indices():
            _data.append([
                #dataset.variable(index = index, name = "eventNumber"),
                dataset.variable(index = index, name = "el_1_pt"),
                #dataset.variable(index = index, name = "el_1_eta"),
                #dataset.variable(index = index, name = "el_1_phi"),
                ##dataset.variable(index = index, name = "jet_1_pt"),
                #dataset.variable(index = index, name = "jet_1_eta"),
                #dataset.variable(index = index, name = "jet_1_phi"),
                ##dataset.variable(index = index, name = "jet_1_e"),
                ##dataset.variable(index = index, name = "jet_2_pt"),
                #dataset.variable(index = index, name = "jet_2_eta"),
                #dataset.variable(index = index, name = "jet_2_phi"),
                ##dataset.variable(index = index, name = "jet_2_e"),
                #dataset.variable(index = index, name = "nJets"),
                ##dataset.variable(index = index, name = "nBTags"),
                ##dataset.variable(index = index, name = "nLjets"),
                ##dataset.variable(index = index, name = "ljet_1_m"),
                #dataset.variable(index = index, name = "met"),
                #dataset.variable(index = index, name = "met_phi"),
                #dataset.variable(index = index, name = "Centrality_all"),
                #dataset.variable(index = index, name = "Mbb_MindR"),            
                #dataset.variable(index = index, name = "ljet_sd23"),
                #dataset.variable(index = index, name = "ljet_tau21"),
                #dataset.variable(index = index, name = "ljet_tau32"),
                #dataset.variable(index = index, name = "Aplan_bjets"),
                #dataset.variable(index = index, name = "H4_all"),
                #dataset.variable(index = index, name = "NBFricoNN_6jin4bin"),
                #dataset.variable(index = index, name = "NBFricoNN_6jin3bex"),
                #dataset.variable(index = index, name = "NBFricoNN_5jex4bin"),
                #dataset.variable(index = index, name = "NBFricoNN_3jex3bex"),
                #dataset.variable(index = index, name = "NBFricoNN_4jin3bex"),
                #dataset.variable(index = index, name = "NBFricoNN_4jin4bin")
            ])
            if apply_class is True:
                _data.append([
                    dataset.variable(name = "class")
                ])
    return Dataset(data = _data)

################################################################################
#                                                                              #
# exchanges data                                                               #
#                                                                              #
################################################################################

class Exchange(object):

    def __init__(
        self,
        utterance                  = None,
        response                   = None,
        utterance_time_UNIX        = None,
        response_time_UNIX         = None,
        utterance_word_vector      = None,
        response_word_vector       = None,
        utterance_reference        = None,
        response_reference         = None,
        exchange_reference         = None
        ):
        self.utterance             = utterance
        self.response              = response
        self.utterance_time_UNIX   = utterance_time_UNIX
        self.response_time_UNIX    = response_time_UNIX
        self.utterance_word_vector = utterance_word_vector,
        self.response_word_vector  = response_word_vector,
        self.utterance_reference   = utterance_reference,
        self.response_reference    = response_reference,
        self.exchange_reference    = exchange_reference,
        self.utterance_word_vector = utterance_word_vector

    def printout(
        self
        ):
        print("exchange:")
        print("utterance: {utterance}".format(
            utterance = self.utterance
        ))
        print("response: {response}".format(
            response = self.response))
        print("utterance_time_UNIX: {utterance_time_UNIX}".format(
            utterance_time_UNIX = self.utterance_time_UNIX
        ))
        print("response_time_UNIX: {response_time_UNIX}".format(
            response_time_UNIX = self.response_time_UNIX
        ))
        print("utterance_word_vector: {utterance_word_vector}".format(
            utterance_word_vector = self.utterance_word_vector
        ))
        print("response_word_vector: {response_word_vector}".format(
            response_word_vector = self.response_word_vector
        ))
        print("utterance_reference: {utterance_reference}".format(
            utterance_reference = self.utterance_reference
        ))
        print("response_reference: {response_reference}".format(
            response_reference = self.response_reference
        ))
        print("exchange_reference: {exchange_reference}".format(
            exchange_reference = self.exchange_reference
        ))

@shijian.timer
def access_exchanges_Reddit(
    user_agent           = "scriptwire",
    subreddits           = None,
    number_of_utterances = 200
    ):
    # Access Reddit.
    log.info("access Reddit API")
    r = praw.Reddit(user_agent = user_agent)
    # Access each subreddit.
    log.info("access subreddits {subreddits}".format(
        subreddits = subreddits
    ))
    for subreddit in subreddits:
        log.info("access subreddit \"{subreddit}\"".format(
            subreddit = subreddit
        ))
        submissions = r.get_subreddit(
            subreddit
        ).get_top(
            limit = int(number_of_utterances)
        )
        # Access each submission, its title and its top comment.
        exchanges = []
        for submission in submissions:
            # Access the submission title.
            submission_title = submission.title.encode(
                "ascii",
                "ignore"
            )
            # Access the submission URL.
            submission_URL = submission.permalink.encode(
                "ascii",
                "ignore"
            )
            # Access the submission time.
            submission_time_UNIX = str(submission.created_utc).encode(
                "ascii",
                "ignore"
            )
            log.debug(
                "access submission \"{submission_title}\"".format(
                subreddit = subreddit,
                submission_title = submission_title
            ))
            comments = praw.helpers.flatten_tree(submission.comments)
            # Save the exchange only if there is a response.
            if comments:
                # Access the submission top comment.
                comment_top_text = comments[0].body.encode(
                    "ascii",
                    "ignore"
                )
                # Access the submission top comment URL.
                comment_top_URL = comments[0].permalink.encode(
                    "ascii",
                    "ignore"
                )
                # Access the submission top comment time.
                comment_top_time_UNIX = str(comments[0].created_utc).encode(
                    "ascii",
                    "ignore"
                )
                # Create a new exchange object for the current exchange data and
                # append it to the list of exchanges.
                exchange = Exchange(
                    utterance           = submission_title,
                    response            = comment_top_text,
                    utterance_time_UNIX = submission_time_UNIX,
                    response_time_UNIX  = comment_top_time_UNIX,
                    utterance_reference = submission_URL,
                    response_reference  = comment_top_URL,
                    exchange_reference  = subreddit
                )
                exchanges.append(exchange)
            # Pause to avoid overtaxing Reddit.
            #time.sleep(2)
    return exchanges

@shijian.timer
def save_exchanges_to_database(
    exchanges = None,
    filename  = "database.db"
    ):
    # Check for the database. If it does not exist, create it.
    if not os.path.isfile(filename):
        log.info("database {filename} nonexistent".format(
            filename = filename
        ))
        log.info("create database {filename}".format(
            filename = filename
        ))
        create_database(filename = filename)
    # Access the database.
    database = access_database(filename = filename)
    # Access or create the exchanges table.
    table_exchanges = database["exchanges"]
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
            table_exchanges.insert(dict(
                utterance          = str(exchange.utterance),
                response           = str(exchange.response),
                utteranceTimeUNIX  = str(exchange.utterance_time_UNIX),
                responseTimeUNIX   = str(exchange.response_time_UNIX),
                utteranceReference = str(exchange.utterance_reference),
                responseReference  = str(exchange.response_reference),
                exchangeReference  = str(exchange.exchange_reference)
            ))
        else:
            log.debug("skip previously-saved exchange \"{utterance}\"".format(
                utterance = exchange.utterance
            ))

@shijian.timer
def convert_exchange_datasets_from_datavision_datasets_to_abstraction_datasets(
    datasets    = None, # a single dataset or a list of datasets
    apply_class = True
    ):
    # If one dataset is specified, contain it in a list.
    if not isinstance(datasets, list):
        datasets = [datasets]
    _data = []
    for dataset in datasets:
        for index in dataset.indices():
            #for variable_name in dataset.variables():
            #    _data.append([
            #        dataset.variable(index = index, name = variable_name),
            #    ])
            _data.append([
                dataset.variable(index = index, name = "utteranceWordVector"),
                dataset.variable(index = index, name = "responseWordVector")
            ])
            if apply_class is True:
                _data.append([
                    dataset.variable(name = "class")
                ])
    return Dataset(data = _data)

################################################################################
#                                                                              #
# neural networks data                                                         #
#                                                                              #
################################################################################

class Dataset(object):

    def __init__(
        self,
        data = None
    ):
        self._data = data

    def features(
        self,
        format_type = "ndarray"
        ):
            if format_type == "ndarray":
                return numpy.asarray(self._data[::2])
            elif format_type == "list":
                return self._data[::2]
            else:
                raise Exception("unknown format requested")

    def targets(
        self,
        format_type = "ndarray"
        ):
            if format_type == "ndarray":
                return numpy.asarray(self._data[1::2])
            elif format_type == "list":
                return self._data[1::2]
            else:
                raise Exception("unknown format requested")

################################################################################
#                                                                              #
# physics objects                                                              #
#                                                                              #
################################################################################

class ROOT_Variable(numpy.ndarray):
 
    def __new__(
        cls,
        name                     = None,
        tree                     = None,
        ):
        self = numpy.asarray([]).view(cls)
        # arguments
        self._name               = name
        self.tree                = tree
        # internal
        self.event_number        = 0
        self.variable_object     = None
        self.variable_type       = None
        self.data_type           = None
        self.variable_data_types = None
        self.canvas              = None
        self.histogram           = None
        self._values             = [] # list of values
        return(self)
 
    @shijian.timer
    def identify_variable(
        self,
        ):
        # Identify the variable data type.
        # Set the identifiable data types.
        self.variable_data_types = {
            "<type 'int'>"                        : "int",
            "<class 'ROOT.vector<float>'>"        : "vector<float>",
            "<class 'ROOT.vector<int>'>"          : "vector<int>",
            "<type 'float'>"                      : "float",
            "<type 'long'>"                       : "long",
            "<type 'ROOT.PyFloatBuffer'>"         : "PyFloatBuffer",
            "<type 'ROOT.PyIntBuffer'>"           : "PyIntBuffer",
            "<class 'ROOT.vector<unsigned int>'>" : "unsigned int"
        }
        # If the variable object exists, check its data type. If there is no
        # variable object, do not set its data type.
        if self.variable_object:
            variable_data_type = str(type(self.variable_object))
        else:
            variable_data_type = None
        if variable_data_type in self.variable_data_types:
            self.data_type = self.variable_data_types[variable_data_type]
            log.debug(
                "variable {name} is identified as data type {data_type}".format(
                    name      = self._name,
                    data_type = self.data_type
                )
            )
        else:
            self.data_type = variable_data_type
            log.warning(
                "variable {name} is of unknown data type {data_type}".format(
                    name      = self._name,
                    data_type = self.data_type
                )
            )
            self.data_type = "vector<float>"
            #self.data_type = "int"
            log.warning("set to default data type {data_type}".format(
                data_type = self.data_type
            ))
 
    @shijian.timer
    def load_variable_object(
        self,
        ):
        if self.tree is None:
            log.error("no tree specified")
            raise(Exception)
        # Set the current event.
        self.tree.GetEntry(self.event_number)
        self.variable_object = getattr(self.tree, self._name)
 
    @shijian.timer
    def load_variable(
        self,
        all_events = True # option to load variable values for all events
        ):
        # Load the variable values.
        log.debug("load variable {name} values".format(name = self._name))
        self._values     = []
        if all_events is None:
            # Load the variable object.
            self.load_variable_object()
            # Identify the variable type and data type.
            self.identify_variable()
            # Use a loading method appropriate to the data type.
            if self.data_type == "int":
                self._values = self.variable_object
            elif self.data_type == "float":
                self._values = self.variable_object
            elif self.data_type == "long":
                self._values = self.variable_object
            else:
                for value in self.variable_object:
                    self._values.append(value)
        else:
            # Load the variable object.
            self.load_variable_object()
            # Identify the variable type and data type.
            self.identify_variable()
            for event in self.tree:
                # Use a loading method appropriate to the data type.
                if self.data_type == "int":
                    self._values.append(self.variable_object)
                elif self.data_type == "float":
                    self._values.append(self.variable_object)
                elif self.data_type == "long":
                    self._values.append(self.variable_object)
                else:
                    for value in self.variable_object:
                        self._values.append(value)
 
    @shijian.timer
    def name(
        self,
        ):
        # return name
        return(self._name)
 
    @shijian.timer
    def values(
        self,
        ):
        # return values
        return(self._values)

@shijian.timer
def select_event(
    event     = None,
    selection = "ejets"
    ):
    """
    Select a HEP event.
    """
    if selection == "ejets":
        # Require single lepton.
        # Require >= 4 jets.
        if \
            0 < len(event.el_pt) < 2 and \
            len(event.jet_pt) >= 4 and \
            len(event.ljet_m) >= 1:
            return True
        else:
            return False

################################################################################
#                                                                              #
# word vectors                                                                 #
#                                                                              #
################################################################################

@shijian.timer
def model_word2vec_Brown_Corpus():
    model_word2vec = Word2Vec(nltk.corpus.brown.sents())
    return model_word2vec

@shijian.timer
def load_word_vector_model(
    filename = None
    ):
    # If an existing word vector model file does not exist, create it.
    if not os.path.isfile(os.path.expandvars(filename)):
        log.error("file {filename} does not exist".format(
            filename = filename
        ))
        log.info("create word vector model and save to file {filename}".format(
            filename = filename
        ))
        model_word2vec = model_word2vec_Brown_Corpus()
        model_word2vec.save(filename)
    else:
        log.info("access file {filename}".format(
            filename = filename
        ))
        model_word2vec = Word2Vec.load(filename)
    return model_word2vec

@shijian.timer
def convert_word_string_to_word_vector(
    word_string    = None,
    model_word2vec = None
    ):
    if word_string in model_word2vec:
        return model_word2vec[word_string]
    else:
        log.debug("word string \"{word_string}\" not in word2vec model".format(
            word_string = word_string
        ))
        return None

@shijian.timer
def convert_sentence_string_to_word_vector(
    sentence_string = None,
    model_word2vec  = None
    ):
    # Convert the sentence string to a list of word strings.
    word_strings = word_list = re.sub("[^\w]", " ",  sentence_string).split()
    # Build a list of word vectors.
    word_vectors = []
    for word_string in word_strings:
        word_vector = convert_word_string_to_word_vector(
            word_string    = word_string,
            model_word2vec = model_word2vec
        )
        if word_vector is not None:
            word_vectors.append(word_vector)
        else:
            log.debug("skip undefined word vector")
    # Combine all of the word vectors into one word vector by summation.
    sentence_word_vector = sum(word_vectors)
    return sentence_word_vector

################################################################################
#                                                                              #
# neural network objects                                                       #
#                                                                              #
################################################################################

@shijian.timer
def draw_neural_network(
    axes        = None,
    left        = None,
    right       = None,
    bottom      = None,
    top         = None,
    layer_sizes = None
    ):
    """
    # abstract

    This function draws a neural network representation diagram using
    matplotilb.

    # arguments

    |*argument* |*description*                                                 |
    |-----------|--------------------------------------------------------------|
    |axes       |matplotlib.axes.AxesSubplot: the axes on which to plot the    |
    |           |diagram (returned by matplotlib.pyplot.gca())                 |
    |left       |float: the position of the centers of the left nodes          |
    |right      |float: the position of the centers of the right nodes         |
    |bottom     |float: the position of the centers of the bottom nodes        |
    |top        |float: the position of the centers of the top nodes           |
    |layer_sizes|list of integers: list of layer sizes, including input and    |
    |           |output dimensionality                                         |

    # example

    ```Python
    figure = matplotlib.pyplot.figure(figsize = (12, 12))
    abstraction.draw_neural_network(
        axes        = figure.gca(),
        left        = .1,
        right       = .9,
        bottom      = .1,
        top         = .9,
        layer_sizes = [4, 7, 2]
    )
    figure.savefig("neural_network_diagram.png")
    ```
    """
    spacing_vertical   = (top - bottom) / float(max(layer_sizes))
    spacing_horizontal = (right - left) / float(len(layer_sizes) - 1)
    # nodes
    for n, layer_size in enumerate(layer_sizes):
        layer_top = spacing_vertical * (layer_size - 1)/2 + (top + bottom) / 2
        for m in xrange(layer_size):
            circle = matplotlib.pyplot.Circle(
                (
                    n * spacing_horizontal + left,
                    layer_top - m * spacing_vertical
                ),
                spacing_vertical / 4,
                color  = "w",
                ec     = "k",
                zorder = 4
            )
            axes.add_artist(circle)
    # edges
    for n, (layer_size_a, layer_size_b) in enumerate(zip(
        layer_sizes[:-1],
        layer_sizes[1:]
        )):
        layer_top_a =\
            spacing_vertical * (layer_size_a - 1) / 2 + (top + bottom) / 2
        layer_top_b =\
            spacing_vertical * (layer_size_b - 1) / 2 + (top + bottom) / 2
        for m in xrange(layer_size_a):
            for o in xrange(layer_size_b):
                line = matplotlib.pyplot.Line2D(
                    [
                        n * spacing_horizontal + left,
                        (n + 1) * spacing_horizontal + left
                    ],
                    [
                        layer_top_a - m * spacing_vertical,
                        layer_top_b - o * spacing_vertical
                    ],
                    c = "k"
                )
                axes.add_artist(line)

class Classification(object):

    def __init__(
        self,
        number_of_classes   = None,
        hidden_nodes        = [10, 20, 10],
        epochs              = 5000,
        batch_size          = 32,
        optimizer           = "SGD",
        learning_rate       = 0.1,
        seed                = 42,
        continue_training   = True,
        load_from_directory = None
    ):
        """
        Create a fully-connected neural network classifier with rectified linear
        unit activators.

        batch_size: number of training examples to use per training step
        """
        if load_from_directory is None:
            self._model = skflow.TensorFlowDNNClassifier(
                n_classes         = number_of_classes,
                hidden_units      = hidden_nodes,
                steps             = epochs,
                batch_size        = batch_size,
                optimizer         = optimizer,
                learning_rate     = learning_rate,
                tf_random_seed    = seed,
                continue_training = True
            )
        else:
            self.load(
                directory = load_from_directory
            )

    def model(self):
        return self._model

    def save(
        self,
        directory = "abstraction_classifier",
        overwrite = False
    ):
        if directory is None:
            directory = shijian.propose_filename(
                filename  = "abstraction_model",
                overwrite = overwrite
            )
        log.info("save model to {directory}".format(
            directory = directory
        ))
        self._model.save(directory)

    def load(
        self,
        directory = "abstraction_classifier"
    ):
        log.info("load model from {directory}".format(
            directory = directory
        ))
        self._model = skflow.TensorFlowEstimator.restore(directory)
        # upcoming:
        # update model instance data attributes from loaded model

class Regression(object):

    def __init__(
        self,
        number_of_classes   = 0,
        hidden_nodes        = [10, 20, 10],
        epochs              = 5000,
        batch_size          = 32,
        optimizer           = "SGD",
        learning_rate       = 0.1,
        seed                = 42,
        continue_training   = True,
        load_from_directory = None
    ):
        """
        Create a fully-connected neural network regressor with rectified linear
        unit activators.

        batch_size: number of training examples to use per training step
        """
        self.hidden_nodes = hidden_nodes
        if load_from_directory is None:
            self._model = skflow.TensorFlowEstimator(
                model_fn          = self.tanh_dnn,
                n_classes         = number_of_classes,
                steps             = epochs,
                batch_size        = batch_size,
                optimizer         = optimizer,
                learning_rate     = learning_rate,
                tf_random_seed    = seed,
                continue_training = True
            )
        else:
            self.load(
                directory = load_from_directory
            )

    def tanh_dnn(
        features     = None,
        targets      = None,
        hidden_nodes = None
    ):
        if hidden_nodes is None:
            hidden_nodes = self.hidden_nodes
        features = skflow.ops.dnn(
            features,
            hidden_units = hidden_nodes,
            activation = skflow.tf.tanh
        )
        return skflow.models.linear_regression(features, targets)

    def model(self):
        return self._model

    def save(
        self,
        directory = "abstraction_regressor",
        overwrite = False
    ):
        if directory is None:
            directory = shijian.propose_filename(
                filename  = "abstraction_model",
                overwrite = overwrite
            )
        log.info("save model to {directory}".format(
            directory = directory
        ))
        self._model.save(directory)

    def load(
        self,
        directory = "abstraction_regressor"
    ):
        log.info("load model from {directory}".format(
            directory = directory
        ))
        self._model = skflow.TensorFlowEstimator.restore(directory)
        # upcoming:
        # update model instance data attributes from loaded model

################################################################################
#                                                                              #
# neural network training                                                      #
#                                                                              #
################################################################################

@shijian.timer
def hypersearch(
    hyperpoints = None,
    dataset     = None,
    train_size  = 0.7,  # fraction of data for training (not testing)
    ):

    log.info("split data for cross-validation")
    features_train, features_test, targets_train, targets_test =\
        sklearn.cross_validation.train_test_split(
            dataset.features(),
            dataset.targets(),
            train_size = train_size
        )

    pyprel.print_line()
    log.info("\nengage hypersearch\n")
    pyprel.print_line()

    log.info("number of hyperpoints: {number_of_hyperpoints}".format(
        number_of_hyperpoints = len(hyperpoints)
    ))
    log.info("hyperpoints: {hyperpoints}".format(
        hyperpoints = hyperpoints
    ))
    pyprel.print_line()

    # Define hypermap.
    hypermap = {}
    hypermap["epoch"]          = []
    hypermap["hidden_nodes"]   = []
    hypermap["score_training"] = []
    hypermap["score_test"]     = []

    progress = shijian.Progress()
    progress.engage_quick_calculation_mode()
    for index, hyperpoint in enumerate(hyperpoints):
        log.info("\nhyperpoint: {hyperpoint}".format(hyperpoint = hyperpoint))

        epoch        = hyperpoint[0]
        hidden_nodes = hyperpoint[1:]

        # define model

        log.info("define classification model")
        classifier = Classification(
            number_of_classes = 2,
            hidden_nodes      = hidden_nodes,
            epochs            = epoch
        )

        # train model

        log.info("fit model to dataset features and targets")
        classifier._model.fit(features_train, targets_train)
        #classifier.save()

        # predict and cross-validate training

        log.info("test trained model on training dataset")
        score_training = sklearn.metrics.accuracy_score(
            classifier._model.predict(features_train),
            targets_train
        )
        score_test = sklearn.metrics.accuracy_score(
            classifier._model.predict(features_test),
            targets_test
        )
        log.info("\ntraining-testing instance complete:")
        log.info("epoch:          {epoch}".format(
            epoch = epoch
        ))
        log.info("architecture:   {architecture}".format(
            architecture = hidden_nodes
        ))
        log.info("score training: {score_training}".format(
            score_training = 100 * score_training
        ))
        log.info("score test:     {score_test}".format(
            score_test = 100 * score_test
        ))
        hypermap["epoch"].append(epoch)
        hypermap["hidden_nodes"].append(hidden_nodes)
        hypermap["score_training"].append(score_training)
        hypermap["score_test"].append(score_test)

        # save current search results
        shijian.export_object(
            hypermap,
            filename  = "hypermap.pkl",
            overwrite = True
        )

        print(progress.add_datum(fraction = (index + 1) / len(hyperpoints)))
        pyprel.print_line()

def analyze_hypermap(
    hypermap                    = None,
    number_of_best_score_models = 6
    ):

    number_of_entries = len(hypermap["epoch"])
    log.info("number of entries: {number_of_entries}".format(
        number_of_entries = number_of_entries
    ))

    # hypermap table

    table_contents = [
        ["epoch", "architecture", "score training", "score testing"]
    ]
    for index in range(0, number_of_entries):
        table_contents.append(
            [
                str(hypermap["epoch"][index]),
                str(hypermap["hidden_nodes"][index]),
                str(hypermap["score_training"][index]),
                str(hypermap["score_test"][index])
            ]
        )
    log.info("\nhypersearch map:\n")
    log.info(
        pyprel.Table(
            contents = table_contents,
        )
    )

    # hypermap table of best score models

    best_models = sorted(zip(
        hypermap["score_test"],
        hypermap["hidden_nodes"]),
        reverse = True
    )[:number_of_best_score_models]
    table_contents = [["architecture", "score testing"]]
    for model in best_models:
        table_contents.append([str(model[1]), str(model[0])])
    log.info("\nbest-scoring models:\n")
    log.info(
        pyprel.Table(
            contents = table_contents,
        )
    )

    # parallel coordinates plot

    number_of_entries = len(hypermap["epoch"])
    datasets = []
    for index in range(0, number_of_entries):
        row = []
        architecture_padded =\
            hypermap["hidden_nodes"][index] +\
            [0] * (5 - len(hypermap["hidden_nodes"][index]))
        row.append(hypermap["epoch"][index])
        row.extend(architecture_padded)
        row.append(hypermap["score_training"][index])
        row.append(hypermap["score_test"][index])
        datasets.append(row)

    datavision.save_parallel_coordinates_matplotlib(
        datasets[::-1],
        filename  = "parallel_coordinates.png",
        directory = "hypermap"
    )

    # parallel coordinates plot of best-scoring models

    best_models = sorted(zip(
        hypermap["score_test"],
        hypermap["score_training"],
        hypermap["hidden_nodes"]),
        reverse = True
    )[:number_of_best_score_models]
    datasets = []
    for model in best_models:
        row = []
        architecture_padded = model[2] + [0] * (5 - len(model[2]))
        row.extend(architecture_padded)
        row.append(model[1])
        row.append(model[0])
        datasets.append(row)

    datavision.save_parallel_coordinates_matplotlib(
        datasets,
        filename  =\
            "parallel_coordinates_"          +\
            str(number_of_best_score_models) +\
            "_best_score_models.png",
        directory = "hypermap"
    )

    # progressive parallel coordinates plots of best-scoring models

    for number_of_datasets_plotted in range(1, number_of_best_score_models):
        datavision.save_parallel_coordinates_matplotlib(
            datasets[:number_of_datasets_plotted],
            filename  =\
                "parallel_coordinates_"           +\
                str(number_of_best_score_models)  +\
                "_best_score_models_progressive_" +\
                str(number_of_datasets_plotted)   +\
                ".png",
            directory = "hypermap"
        )

    ## plot
    #
    #architectures = shijian.unique_list_elements(hypermap["hidden_nodes"])
    #
    #architecture_epoch_score = {}
    #for architecture in architectures:
    #    architecture_epoch_score[str(architecture)] = []
    #    for index in range(0, number_of_entries):
    #        if hypermap["hidden_nodes"][index] == architecture:
    #            architecture_epoch_score[str(architecture)].append(
    #                [
    #                    hypermap["epoch"][index],
    #                    hypermap["score_test"][index]
    #                ]
    #            )
    #
    #figure = matplotlib.pyplot.figure()
    #figure.set_size_inches(10, 10)
    #axes = figure.add_subplot(1, 1, 1)
    #axes.set_xscale("log")
    #figure.suptitle("hyperparameter map", fontsize = 20)
    #matplotlib.pyplot.xlabel("epochs")
    #matplotlib.pyplot.ylabel("training test score")
    #
    #for key, value in architecture_epoch_score.iteritems():
    #    epochs     = [element[0] for element in value]
    #    score_test = [element[1] for element in value]
    #    matplotlib.pyplot.plot(epochs, score_test, label = key)
    #
    #matplotlib.pyplot.legend(
    #    loc            = "center left",
    #    bbox_to_anchor = (1, 0.5),
    #    fontsize       = 10
    #)
    #
    #matplotlib.pyplot.savefig(
    #    "hyperparameter_map.eps",
    #    bbox_inches = "tight",
    #    format      = "eps"
    #)