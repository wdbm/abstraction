# abstraction

[![project abstraction](http://img.youtube.com/vi/v9zJ9noLeok/0.jpg)](https://www.youtube.com/watch?v=v9zJ9noLeok)

# setup

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

|**prerequisite**|**comment**|
|---|---|
|SQLite|```sudo apt-get -y install sqlite```|
|docopt|```sudo pip install docopt```|
|technicolor|[technicolor](https://github.com/wdbm/technicolor)|
|PRAW|```sudo pip install praw```|
|dataset|```sudo pip install dataset```|

# introduction

Project abstraction is a natural language processing project utilising curated conversation data as neural network training data.

# bags of words, skip-grams and word vectors

Word vectors are an efficient implementation of bag-of-words and skip-gram architectures for computing vector representations of words. These representations can be used in natural language processing applications and research.

An n-gram is a contiguous sequence of n items from a sequence of text or speech. The items can be phonemes, syllabels, letters, words or base pairs depending on the application. Skip-grams are a generalisation of n-grams in which the components (typically words) need not be consecutive in the text under consideration, but may have gaps that are skipped. They are one way of overcoming the data sparsity problem found in conventional n-gram analysis.

Formally, an n-gram is a consecutive subsequence of length n of some sequence of tokens w_n. A k-skip-n-gram is a length-n subsequence in which components occur at a distance of at most k from each other. For example, in the text

    the rain in Spain falls mainly on the plain

the set of 1-skip-2-grams includes all of the 2-grams and, in addition, the following sequences:

    the in,
    rain Spain,
    in falls,
    Spain mainly,
    mainly the,
    on plain

It has been demonstrated that skip-gram language models can be trained such that it is possible to perform 'word arithmetic'. For example, with an appropriate model, the expression ```king - man + woman``` evaluates to very close to ```queen```.

- "Efficient Estimation of Word Representations in Vector Space", Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean <http://arxiv.org/abs/1301.3781>

The bag-of-words model is a simplifying representation used in natural language processing. In this model, a text is represented as a bag (multiset -- a set in which members can appear more than once) of its words, disregarding grammar and word order but keeping multiplicity. The bag-of-words model is used commonly in methods of document classification, for which the frequency of occurrence of each word is used as a feature for training a classifier.

Word vectors are continuous distributed representations of words. The tool word2vec takes a text corpus as input and produces word vectors as output. It constructs a vocabulary from the training text data and then learns vector representations of words. A word2vec model is formed by training on raw text. It records the context, or usage, of each word encoded as word vectors. The significance of a word vector is defined as its usefulness as an indicator of certain larger meanings or labels.

# curated conversation data

Curated conversation data sourced from Reddit is used for the conversation analysis and modelling. Specifically, conversational exchanges on Reddit are recorded. An exchange consists of an utterance and a response to the utterance, together with associated data, such as references and timestamps. A submission to Reddit is considered as an utterance and a comment on the submission is considered as a response to the utterance. The utterance is assumed to be of good quality and the response is assumed to be appropriate to the utterance based on the crowd-curated quality assessment inherent in Reddit.

# module abstraction

The module abstraction contains functions used generally for project abstraction. Many of the programs of the project use its functions.

# arcodex: archive collated exchanges

The program arcodex is a data collation and archiving program specialised to conversational exchanges. It can be used to archive to database exchanges on Reddit.

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

The standard run 2014-10-28T202832Z is as follows:

```Bash
arcodex.py --numberOfUtterances 200 --subreddits=askreddit,changemyview,lgbt,machinelearning,particlephysics,technology,worldnews --verbose
```

# vicodex: view collated exchanges

The program vicodex is a viewing program specialised to conversational exchanges. It can be used to access and view a database of exchanges.

The following example accesses database "database.db" and displays its exchanges data:

```Bash
vicodex.py --database="database.db"
```

# reducodex: remove duplicate collated exchanges                        

The program reducodex inspects an existing database of conversational exchanges, removes duplicate entries, creates simplified identifiers for entries and then writes a new database of these entries.          

The following examples access database "database.db", remove duplicate entries, create simplified identifiers for entries and output database "database_1.db":

```Bash
reducodex.py --inputdatabase="database.db"
```

```Bash
reducodex.py --inputdatabase="database.db" --outputdatabase="database_1.db"
```
