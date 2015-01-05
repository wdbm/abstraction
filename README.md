# abstraction

# introduction

This is a natural language processing project utilising curated conversation data as neural network training data.

## quick start

The following Bash commands, that have been tested on Ubuntu 14.10, should install prerequisites and check out abstraction.

```Bash
sudo pip install docopt
sudo pip install pyfiglet
git clone https://github.com/wdbm/abstraction.git
cd abstraction/
wget https://raw.githubusercontent.com/wdbm/pyprel/master/pyprel.py
wget https://raw.githubusercontent.com/wdbm/shijian/master/shijian.py
wget https://raw.githubusercontent.com/wdbm/technicolor/master/technicolor.py
```

# prerequisites

## SQLite

```Bash
sudo apt-get -y install sqlite
```

## docopt

```Bash
sudo pip install docopt
```

## technicolor

- [technicolor](https://github.com/wdbm/technicolor)

## PRAW

```Bash
sudo pip install praw
```

## dataset

```Bash
sudo pip install dataset
```

# arcodex: archive collated exchanges

The program arcodex is a data collation and archiving program specialised to conversational exchanges. It can be used to access and archive to database exchanges on Reddit. An exchange consists of an utterance and a response to the utterance, together with associated data, such as references and timestamps. A submission to Reddit is considered as an utterance and a comment on the submission is considered as a response to the utterance. The utterance is assumed to be of good quality and the response is assumed to be appropriate to the utterance based on the crowd-curated quality assessment inherent in Reddit.

## usage examples

The following example accesses 2 utterances from the subreddit "worldnews" with verbosity:

```Bash
arcodex.py --numberOfUtterances 2 --subreddits=worldnews --verbose
```

The following example accesses 2 utterances from each of the subreddits "changemyview" and "worldnews" with verbosity:

```Bash
arcodex.py --numberOfUtterances 2 --subreddits=changemyview,worldnews --verbose
```

The following example accesses 30 utterances from all of the listed subreddits with verbosity:

```Bash
arcodex.py --numberOfUtterances 30 --subreddits=askreddit,changemyview,lgbt,machinelearning,particlephysics,technology,worldnews --verbose
```

# vicodex: view collated exchanges

The program vicodex is a viewing program specialised to conversational exchanges. It can be used to access and view a database of exchanges.

## usage examples

The following example accesses database "database.db" and displays its exchanges data:

```Bash
vicodex.py --database="database.db"
```
