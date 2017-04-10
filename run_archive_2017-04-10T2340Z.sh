#!/bin/bash

python arcodex.py --numberOfUtterances 200 --subreddits=askreddit,changemyview,lgbt,machinelearning,particlephysics,technology,worldnews --verbose #--database=""$(date "+%Y-%m-%dT%H%MZ" --utc)".db"


IFS= read -d '' text << "EOF"
import abstraction
abstraction.save_tweets_of_top_followed_users_Twitter_to_database()
EOF

echo -e "\nrun the following code:\n"
echo "${text}"
