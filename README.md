# abstraction

## introduction

This is a natural language processing project utilising curated conversation data as neural network training data.

# prerequisites

## SQLite

    sudo apt-get -y install sqlite

## docopt

    sudo pip install docopt

## technicolor

    - [technicolor](https://github.com/wdbm/technicolor)

## PRAW

    sudo pip install praw

## dataset

    sudo pip install dataset

# arcodex: archive collated exchanges

The program arcoex is a data collation and archiving program specialised to conversational exchanges. It can be used to access and archive to database exchanges on Reddit. An exchange consists of an utterance and a response to the utterance, together with associated data, such as references and timestamps. A submission to Reddit is considered as an utterance and a comment on the submission is considered as a response to the utterance. The utterance is assumed to be of good quality and the response is assumed to be appropriate to the utterance based on the crowd-curated quality assessment inherent in Reddit.

## usage examples

The following example accesses 2 utterances from the subreddit "worldnews" with verbosity:

    arcodex.py --numberOfUtterances 2 --subreddits=worldnews --verbose

The following example accesses 2 utterances from each of the subreddits "changemyview" and "worldnews" with verbosity:

    arcodex.py --numberOfUtterances 2 --subreddits=changemyview,worldnews --verbose

The following example accesses 30 utterances from all of the listed subreddits with verbosity:

    arcodex.py --numberOfUtterances 30 --subreddits=askreddit,changemyview,lgbt,machinelearning,particlephysics,technology,worldnews --verbose
