# data_scipts

This will contain scripts used to process and clean the Enron email data.

## init_database.py

Creates a mysql database and then populates it using a given script. Must have mysql installed.

### Usage

Run this on the command line as follows:

python init_database.py --host [mysql hostname] --user [mysql username] --passwd [mysql password] --name [database name, ie. enron] --query_path [ie. "../data/enron.sql"]
