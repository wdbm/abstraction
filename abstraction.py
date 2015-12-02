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

version = "2015-12-02T1425Z"

import os
import sys
import subprocess
import time
import datetime
import re
import logging
import inspect
import pyprel
import shijian
import dataset
import praw
import math
import numpy
import matplotlib
import matplotlib.pyplot
from gensim.models import Word2Vec
import nltk

log = logging.getLogger(__name__)

def setup():
    # Download NLTK data.
    downloader = nltk.downloader.Downloader("http://nltk.github.com/nltk_data/")
    downloader.download("all")

def model_word2vec_Brown_Corpus():
    model_word2vec = Word2Vec(nltk.corpus.brown.sents())
    return model_word2vec

def convert_word_string_to_word_vector(
    wordString     = None,
    model_word2vec = None
    ):
    if wordString in model_word2vec:
        return model_word2vec[wordString]
    else:
        log.debug("word string \"{wordString}\" not in word2vec model".format(
            wordString = wordString
        ))
        return None

def convert_sentence_string_to_word_vector(
    sentenceString = None,
    model_word2vec = None
    ):
    # Convert the sentence string to a list of word strings.
    wordStrings = wordList = re.sub("[^\w]", " ",  sentenceString).split()
    # Build a list of word vectors.
    wordVectors = []
    for wordString in wordStrings:
        wordVector = convert_word_string_to_word_vector(
            wordString     = wordString,
            model_word2vec = model_word2vec
        )
        if wordVector is not None:
            wordVectors.append(wordVector)
        else:
            log.debug("skip undefined word vector")
    # Combine all of the word vectors into one word vector by summation.
    sentenceWordVector = sum(wordVectors)
    return sentenceWordVector

def create_database(
    fileName = None
    ):
    os.system(
        "sqlite3 " + \
        fileName + \
        " \"create table aTable(field1 int); drop table aTable;\""
    )

def access_database(
    fileName = "database.db"
    ):
    # Access the database.
    log.debug("access database \"{fileName}\"".format(
        fileName = fileName
    ))
    database = dataset.connect("sqlite:///" + fileName)
    return database

def save_database_metadata(
    fileName = "database.db"
    ):
    database = access_database(fileName = fileName)
    # Access or create the metadata table, delete it and then recreate it.
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
        version              = "2015-01-06T172242Z",
        lastModificationTime = currentTime
    )
    log.debug("database metadata:")
    log.debug(pyprel.dictionaryString(dictionary = metadata))
    # Save metadata to database.
    log.debug("save database metadata")
    tableMetadata.insert(metadata)

def database_metadata(
    fileName = "database.db"
    ):
    database = access_database(fileName = fileName)
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

def log_database_metadata(
    fileName = "database.db"
    ):
    metadata = database_metadata(fileName = fileName)
    log.info(pyprel.dictionaryString(dictionary = metadata))

class Exchange(object):

    def __init__(
        self,
        utterance                = None,
        response                 = None,
        utteranceTimeUNIX        = None,
        responseTimeUNIX         = None,
        utteranceWordVector      = None,
        responseWordVector       = None,
        utteranceReference       = None,
        responseReference        = None,
        exchangeReference        = None
        ):
        self.utterance           = utterance
        self.response            = response
        self.utteranceTimeUNIX   = utteranceTimeUNIX
        self.responseTimeUNIX    = responseTimeUNIX
        self.utteranceWordVector = utteranceWordVector,
        self.responseWordVector  = responseWordVector,
        self.utteranceReference  = utteranceReference,
        self.responseReference   = responseReference,
        self.exchangeReference   = exchangeReference,
        self.utteranceWordVector = utteranceWordVector

    def printout(
        self
        ):
        print("exchange:")
        print("utterance: {utterance}".format(
            utterance = self.utterance
        ))
        print("response: {response}".format(
            response = self.response))
        print("utteranceTimeUNIX: {utteranceTimeUNIX}".format(
            utteranceTimeUNIX = self.utteranceTimeUNIX
        ))
        print("responseTimeUNIX: {responseTimeUNIX}".format(
            responseTimeUNIX = self.responseTimeUNIX
        ))
        print("utteranceWordVector: {utteranceWordVector}".format(
            utteranceWordVector = self.utteranceWordVector
        ))
        print("responseWordVector: {responseWordVector}".format(
            responseWordVector = self.responseWordVector
        ))
        print("utteranceReference: {utteranceReference}".format(
            utteranceReference = self.utteranceReference
        ))
        print("responseReference: {responseReference}".format(
            responseReference = self.responseReference
        ))
        print("exchangeReference: {exchangeReference}".format(
            exchangeReference = self.exchangeReference
        ))

def access_exchanges_Reddit(
    userAgent          = "scriptwire",
    subreddits         = None,
    numberOfUtterances = 200
    ):
    # Access Reddit.
    log.info("access Reddit API")
    r = praw.Reddit(user_agent = userAgent)
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
            limit = int(numberOfUtterances)
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
                "access submission \"{submissionTitle}\"".format(
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
    return exchanges

def save_exchanges_to_database(
    exchanges = None,
    fileName  = "database.db"
    ):
    # Check for the database. If it does not exist, create it.
    if not os.path.isfile(fileName):
        log.info("database {fileName} nonexistent".format(
            fileName = fileName
        ))
        log.info("create database {fileName}".format(
            fileName = fileName
        ))
        create_database(fileName = fileName)
    # Access the database.
    database = access_database(fileName = fileName)
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
                utterance          = str(exchange.utterance),
                response           = str(exchange.response),
                utteranceTimeUNIX  = str(exchange.utteranceTimeUNIX),
                responseTimeUNIX   = str(exchange.responseTimeUNIX),
                utteranceReference = str(exchange.utteranceReference),
                responseReference  = str(exchange.responseReference),
                exchangeReference  = str(exchange.exchangeReference)
            ))
        else:
            log.debug("skip previously-saved exchange \"{utterance}\"".format(
                utterance = exchange.utterance
            ))

def load_word_vector_model(
    fileName = None
    ):
    # If an existing word vector model file does not exist, create it.
    if not os.path.isfile(os.path.expandvars(fileName)):
        log.error("file {fileName} does not exist".format(
            fileName = fileName
        ))
        log.info("create word vector model and save to file {fileName}".format(
            fileName = fileName
        ))
        model_word2vec = model_word2vec_Brown_Corpus()
        model_word2vec.save(fileName)
    else:
        log.info("access file {fileName}".format(
            fileName = fileName
        ))
        model_word2vec = Word2Vec.load(fileName)
    return model_word2vec

def ensure_file_existence(fileName):
    log.debug("ensure existence of file {fileName}".format(
        fileName = fileName
    ))
    if not os.path.isfile(os.path.expandvars(fileName)):
        log.error("file {fileName} does not exist".format(
            fileName = fileName
        ))
        program.terminate()
        raise Exception
    else:
        log.debug("file {fileName} found".format(
            fileName = fileName
        ))

def dot_product(v1, v2):
    return(sum((a*b) for a, b in zip(v1, v2)))

def magnitude(v):
    return(numpy.linalg.norm(v))
    #return(math.sqrt(dot_product(v, v)))

def angle(v1, v2):
    cosine = dot_product(v1, v2) / (magnitude(v1) * magnitude(v2))
    cosine = 1 if cosine > 1 else cosine
    return(math.acos(cosine))

def add_exchange_word_vectors_to_database(
    fileName       = "database.db",
    model_word2vec = None
    ):
    # Ensure that the database exists.
    if not os.path.isfile(fileName):
        log.info("database {fileName} nonexistent".format(
            fileName = fileName
        ))
        program.terminate()
        raise Exception
    # Access the database.
    database = access_database(fileName = fileName)
    # Access or create the exchanges table.
    tableExchanges = database["exchanges"]
    # Access exchanges.
    tableName = "exchanges"
    # progress
    progress = shijian.Progress()
    progress.engage_quick_calculation_mode()
    numberOfEntries = len(database[tableName])
    for entryIndex, entry in enumerate(database[tableName].all()):
        uniqueIdentifier = str(entry["id"])
        # Create word vector representations of utterances and responses and
        # add them or update them in the database.
        try:
            utteranceWordVectorNumPyArray = numpy.array_repr(
                convert_sentence_string_to_word_vector(
                    sentenceString = str(entry["utterance"]),
                    model_word2vec = model_word2vec
                )
            )
            responseWordVectorNumPyArray = numpy.array_repr(
                convert_sentence_string_to_word_vector(
                    sentenceString = str(entry["response"]),
                    model_word2vec = model_word2vec
                )
            )
            data = dict(
                id                  = uniqueIdentifier,
                utteranceWordVector = utteranceWordVectorNumPyArray,
                responseWordVector  = responseWordVectorNumPyArray
            )
        except:
            data = dict(
                id                  = uniqueIdentifier,
                utteranceWordVector = None,
                responseWordVector  = None
            )
        database[tableName].update(data, ["id"])
        print progress.add_datum(fraction = entryIndex / numberOfEntries),

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
