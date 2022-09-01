This repository uses a google bigquery public database to query information about blocks on the bitcoin block chain.

As such you must have a google service account key and set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to that key inorder to query the database nessesary for this code to function.



This table can be viewed at

https://www.kaggle.com/datasets/bigquery/bitcoin-blockchain?select=blocks


As of the time of this writing these two files give the following answers:

Probability of a block being mined 2 hours after the previous block: `0.000420241312475818%`

Total consecutive blocks mines more than 2 hours apart: `14600`