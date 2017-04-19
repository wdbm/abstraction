#!/bin/bash

version="2017-04-19T1049Z"

python arcodex.py --numberOfUtterances 200 --subreddits=askreddit,changemyview,lgbt,machinelearning,particlephysics,technology,worldnews --verbose #--database=""$(date "+%Y-%m-%dT%H%MZ" --utc)".db"

cp Twitter.db ""$(date "+%Y-%m-%dT%H%MZ" --utc)"_backup_Twitter.db"
python abstraction_save_tweets_of_top_followed_users_Twitter_to_database.py
mv Twitter.db Twitter_0.db
duplicates_database_SQLite.py --databasein=Twitter_0.db --databaseout=Twitter.db
#rm Twitter_0.db
