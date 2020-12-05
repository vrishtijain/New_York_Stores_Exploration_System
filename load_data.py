#Your application needs to define a script to load the data 
# (e.g., load_data.py). It should create your schema, 
# read the data files, and load the data into the database appropriately. 
# It should be able to run from the command line with no additional arguments.
import psycopg2
import preprocessing
import load
# creating schema
def load_everything():
    # loadign scheme
    connection_string = " user = 'project' password = 'project'  host = '127.0.0.1'  port = '5432' dbname = 'project' "
    conn = psycopg2.connect(connection_string)
    with conn.cursor() as cursor:
        setup_queries = open('schema.sql', 'r').read()
        cursor.execute(setup_queries)
        conn.commit()
    # preprocess the data
    preprocessing.preprocess()
    # loading csv into database
    load.load_into_database()
    

if __name__ == "__main__":
    load_everything()
    
