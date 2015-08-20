[![project abstraction](http://img.youtube.com/vi/v9zJ9noLeok/0.jpg)](https://www.youtube.com/watch?v=v9zJ9noLeok)

# setup

## quick start

The following Bash commands, that have been tested on Ubuntu 14.10, should install prerequisites and check out abstraction.

```Bash
sudo pip install docopt
sudo pip install pyfiglet
sudo pip install praw
sudo apt-get -y install sqlite
sudo pip install dataset
sudo apt-get -y install python-nltk
sudo python -m nltk.downloader all
sudo easy_install -U gensim
git clone https://github.com/wdbm/abstraction.git
cd abstraction/
wget https://raw.githubusercontent.com/wdbm/pyprel/master/pyprel.py
wget https://raw.githubusercontent.com/wdbm/shijian/master/shijian.py
wget https://raw.githubusercontent.com/wdbm/technicolor/master/technicolor.py
```

# prerequisites

|**prerequisite**|**comment**|
|---|---|
|docopt|```sudo pip install docopt```|
|pyfiglet|```sudo pip install pyfiglet```|
|pyprel|[pyprel](https://github.com/wdbm/pyprel)|
|shijian|[shijian](https://github.com/wdbm/shijian)|
|technicolor|[technicolor](https://github.com/wdbm/technicolor)|
|PRAW|```sudo pip install praw```|
|SQLite|```sudo apt-get -y install sqlite```|
|dataset|```sudo pip install dataset```|
|NLTK|```sudo apt-get -y install python-nltk```|
|NLTK data|```sudo python -m nltk.downloader all```|
|gensim|```sudo easy_install -U gensim```|

The function ```abstraction.setup()``` should be run.

# Caffe infrastructure setup

```Bash
sudo apt-get -y install libprotobuf-dev
sudo apt-get -y install libleveldb-dev
sudo apt-get -y install libsnappy-dev
sudo apt-get -y install libopencv-dev
sudo apt-get -y install libhdf5-dev
sudo apt-get -y install libhdf5-serial-dev
sudo apt-get -y install protobuf-compiler
sudo apt-get -y install --no-install-recommends libboost-all-dev
sudo apt-get -y install libatlas-base-dev
sudo apt-get -y install python-dev
sudo apt-get -y install libgflags-dev libgoogle-glog-dev liblmdb-dev
```

```Bash
sudo pip install protobuf
sudo pip install scikit-image
```

```Bash
cd
git clone https://github.com/BVLC/caffe.git
cd caffe
cp Makefile.config.example Makefile.config
```

Edit the makefile. Uncomment ```CPU_ONLY := 1``` for a non-GPU compilation (without CUDA). It may be necessary to include the following lines:

```
INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include /usr/include/hdf5/serial/
LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib /usr/lib/x86_64-linux-gnu/hdf5/serial
```

```Bash
time make all
time make test
time make runtest
time make pycaffe
```

```Bash
PYTHONPATH="/home/"${USER}"/caffe/python:${PYTHONPATH}"
CAFFE="/home/"${USER}"/caffe"
```

Download Caffe models from the Model Zoo.

- <http://caffe.berkeleyvision.org/model_zoo.html>
- <https://github.com/BVLC/caffe/wiki/Model-Zoo>

```Bash
~/caffe/scripts/download_model_binary.py models/bvlc_googlenet
```

# CPU versus GPU for deep learning

Roelof Pieters set some benchmarks in 2015-07 for deep dreaming video processing using CPU and GPU hardware. The CPU hardware was Amazon EC2 g2.2xlarge Intel Xeon E5-2670 (Sandy Bridge) 8 cores 2.6 GHz/3.3 GHz turbo and the GPU hardware was Amazon EC2 g2.2xlarge 2 x 4 Gb GPU.

|**input image resolution (pixels)**|**CPU processing time for 1 image**|**GPU processing time for 1 image**|**CPU processing time for 2 minute video**|**GPU processing time for 2 minute video**|
|---|---|---|---|---|
|540 x 360|45 s|1 s|1 d 21 h|60 minutes|
|1024 x 768|144 s|3 s|6 d|3 h|

So, the GPU hardware was ~45 -- ~48 times faster than the CPU hardware.

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

# abstraction code picture

![](packages_abstraction.png)

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
