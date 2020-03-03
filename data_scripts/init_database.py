import mysql.connector
import argparse
import sys

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-hs', '--host', required=True)
    parser.add_argument('-u', '--user', required=True)
    parser.add_argument('-p', '--passwd', required=True)
    parser.add_argument('-n', '--name', required=True)
    parser.add_argument('-q', '--query_path', required=True)
    args = parser.parse_args()
    return args.host, args.user, args.passwd, args.name, args.query_path

def database_exist(cursor, name):
    """
    Return True if database with NAME exist, else False.
    name: str, database name
    cursor: CMySQLCursor, cursor to database
    """

    cursor.execute("SHOW DATABASES")
    databases = [db[0] for db in cursor]
    return name in databases

def get_query(query_path):
    """
    Given a file path to a query, reads and returns the contents.
    query_path: str, location of query file
    """
    try:
        f = open(query_path, mode='rb')
        query = f.read()
        f.close()
        return query
    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror}")
    except:
        print(f"Unexpected error: {sys.exc_info()[0]}")
        raise

def create_database(host, user, passwd, name):
    """
    Create database NAME if it does not already exist.
    host: str, hostname
    user: str, username
    passwd: str, password
    name: str, database name
    """
    print(f"Creating database {name}..")
    db = mysql.connector.connect(
            host=host, user=user, passwd=passwd
        )
    cursor = db.cursor()

    if database_exist(cursor, name):
        # TODO: OPTION TO OVERRIDE?
        print(f"Database {name} already exist.")
    else:
        create_db_query = f"CREATE DATABASE {name}"
        cursor.execute(create_db_query)
        db.commit()
        print(f"Database {name} successfully created.")
    cursor.close()
    db.close()

def populate_database(host, user, passwd, name, query_path):
    """
    Populate database NAME using query stored in QUERY_PATH.
    host: str, hostname
    user: str, username
    passwd: str, password
    name: str, database name
    query_path: str, path to query
    """
    print(f"Connecting to database {name}..")
    db = mysql.connector.connect(
            host=host, user=user, passwd=passwd, database=name
        )
    cursor = db.cursor()
    print(f"Successfully connected to database {name}.")

    print(f"Retreiving query at {query_path} ..")
    query = get_query(query_path)
    print(f"Setting max_allowed_packet..")
    cursor.execute("SET GLOBAL max_allowed_packet=128M;")
    print(f"Executing query..")
    cursor.execute(query)
    print(f"Executing query to database {name}..")
    db.commit()
    print(f"Successfully executed query.")
    cursor.close()
    db.close()

if __name__ == '__main__':
    host, user, passwd, name, query_path = get_args()
    create_database(host, user, passwd, name)
    populate_database(host, user, passwd, name, query_path)
