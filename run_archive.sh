#!/bin/bash

version="2017-04-14T1845Z"

python arcodex.py --numberOfUtterances 200 --subreddits=askreddit,changemyview,lgbt,machinelearning,particlephysics,technology,worldnews --verbose #--database=""$(date "+%Y-%m-%dT%H%MZ" --utc)".db"

python abstraction_save_tweets_of_top_followed_users_Twitter_to_database.py
duplicates_database_SQLite.py --databasein=Twitter.db --databaseout=Twitter_1.db
rm Twitter.db
mv Twitter_1.db Twitter.db
