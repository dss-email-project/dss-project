import pandas as pd
import email
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inpath', required=True)
    parser.add_argument('-o', '--outpath', required=True)
    args = parser.parse_args()
    return args.inpath, args.outpath

def parse_data(emails, df):
    """ Creates a new column in df for every key in emails
    emails: email object
    df: DataFrame to add column to
    """
    fields = emails[0].keys()
    for field in fields:
        field_series = []
        for email in emails:
            field_series.append(email[field])
        df[field] = field_series

def create_messages_column(emails, df):
    """ Adds column `message` to df containing the email's content
    emails: email object
    df: DataFrame to add column to
    """
    msgs = []
    for email in emails:
        msg = email.get_payload()
        msg = msg.replace('\n',' ')
        msg = msg.replace('\t',' ')
        msgs.append(msg)
    df['message'] = msgs

if __name__ == "__main__":
    inpath, outpath = get_args()

    # Load csv located at inpath
    print("Loading file {inpath} ..")
    emails_df = pd.read_csv(inpath)
    emails_df.rename(columns={'message':'data'}, inplace=True)

    # Convert content in emails['data'] to email objects
    print("Parsing email content..")
    email_objs = list(map(email.message_from_string, emails_df['data']))

    # Extract email messages and store in new column
    create_messages_column(email_objs, emails_df)

    # Extract all other email fields and store in new columns
    parse_data(email_objs, emails_df)    

    # Drop unneeded column
    emails_df.drop(columns='data', inplace=True)

    # Save DataFrame to CSV file
    print(f"Saving to {outpath} ..")
    emails_df.to_csv(outpath)
    print("Succesfully parsed and saved data.")