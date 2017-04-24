# usage

# logging

Updating logging procedures is under consideration because of possible logging conflicts. It could be beneficial currently to run using Bash anonymous pipes, in a way like the following:

```Bash
python script.py 2> >(grep -E -v "INFO|DEBUG")
```

TensorFlow log level can be changed to exclude warnings:

```Bash
export TF_CPP_MIN_LOG_LEVEL=2
```

# examining databases

A database can be examined using [datavision](https://github.com/wdbm/datavision) [view_database_SQLite.py](https://github.com/wdbm/datavision/blob/master/view_database_SQLite.py).

# module abstraction

The module abstraction contains functions used generally for project abstraction. Many of the programs of the project use its functions.

# arcodex: archive collated exchanges

The program arcodex is a data collation and archiving program specialized to conversational exchanges. It can be used to archive to database exchanges on Reddit.

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

# vicodex, vicodex_2: view collated exchanges

The program vicodex_2 (and vicodex) is a viewing program specialized to conversational exchanges. It can be used to access and view a database of exchanges.

The following example accesses database `database.db` and displays its exchanges data:

```Bash
vicodex_2.py --database="database.db"
```

# inspect-database: quick printout of database

The program inspect-database provides a simple, comprehensive printout of the contents of a database. Specifically, for every table in the database it prints all of the column contents for every entry.

```Bash
inspect-database.py --database="database.db"
```

The program Sqliteman can be used to provide a view of database information:

```Bash
sqliteman database.db
```

```
SELECT * FROM exchanges;
```

# vcodex: word vectors 

The program vcodex converts conversational exchanges in an abstraction database to word vector representations and adds or updates an abstraction database with these vectors.          

```Bash
vcodex.py --database="database.db" --wordvectormodel=Brown_corpus.wvm
```

The program vcodex increases the file size of abstraction database version 2015-01-06T172242Z by a factor of ~5.49. On an i7-5500U CPU running at 2.40 GHz, the conversion rate is ~25 exchanges per second.

# reducodex: remove duplicate collated exchanges

The program reducodex inspects an existing database of conversational exchanges, removes duplicate entries, creates simplified identifiers for entries and then writes a new database of these entries.          

The following examples access database "database.db", remove duplicate entries, create simplified identifiers for entries and output database "database_1.db":

```Bash
reducodex.py --inputdatabase="database.db"
```

```Bash
reducodex.py --inputdatabase="database.db" --outputdatabase="database_1.db"
```

# fix_database: fix the data structures of database entries

```Bash
fix_database.py --verbose 2> >(grep -E -v "INFO|DEBUG")
```

# abstraction development testing

```Bash
./arcodex.py --numberOfUtterances 10 --subreddits=askreddit,changemyview,lgbt,machinelearning,particlephysics,technology,worldnews --database=2015-10-12T1612Z.db --verbose
```

```Bash
./vicodex.py --database=2015-10-12T1612Z.db
```

# saving models

Note that the file `checkpoint` in the saved model directory contains full paths.

# run_archive.sh

This is a regular archiving script (for Reddit, Twitter etc.). It can be run every 24 hours using the following procedure, which is available using script `run_archive_loop_24_hours.sh`:

```Bash
while true; do
    ./run_archive.sh
    sleep 86400
done
```
