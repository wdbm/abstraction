#!/bin/bash

python arcodex.py --numberOfUtterances 200 --subreddits=askreddit,changemyview,lgbt,machinelearning,particlephysics,technology,worldnews --verbose #--database=""$(date "+%Y-%m-%dT%H%MZ" --utc)".db"
