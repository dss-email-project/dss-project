# data_scripts

This will contain scripts used to process and clean the Enron email data.

## init_database.py

Creates a mysql database and then populates it using a given script. Must have mysql installed.

### Usage

Run this on the command line as follows:

python init_database.py --host [mysql hostname] --user [mysql username] --passwd [mysql password] --name [database name, ie. enron] --query_path [ie. "../data/enron.sql"]

Example:

python init_database.py --host hstnme --user root --passwd ***** --name enron --query_path data/enron.sql

## parse_data.py

Takes the Kaggle Enron Email CSV file and parses the information into a new, organized CSV file. The Kaggle file has two columns: 'file' and 'message'. Column 'message' contains the email content and metadata. The script parses the 'message' column into several columns for easier use. 

*For a more in-depth understanding with previews of the data, look at parse_data.ipynb.*

### Usage

Run this on the command line as follows:

python parse_data.py --inpath | -i [path to input csv file] --outpath | -o [path to output csv file]

Example:

python parse_data.py -i data/emails.csv -o data/emails_parsed.py

*Note*: *outfile* will be created if it does not already exist.

