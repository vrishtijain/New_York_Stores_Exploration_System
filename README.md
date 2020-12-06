# Store Exploration System

Members
Vrishti Jain (jainv)
Ridhi Gulati (gulatr)

## Database Setup

All the required datasets are in the "Dataset" folder
To setup the database locally:
1. Login as 'Postgres' using:
   psql -U postgres
   
2. Run db-setup.sql as a super user:
   psql -U postgres postgres <- db-setup.sql
   This creates project user and grant the required priveleges.

## Loading Data

The data can be loaded by:
 
 1. Run `retreive_data.py` to download the required datasets.

 2. Run `load_data.py` to load the dataset. This internally runs `schema.sql` and creates the schema for the database. 
    Next, `preprocessing.py` and `load.py` loads the final dataset used in the project.

## Running the Application

To run the application run `application.py` file.


## Dependencies

`requirements.txt` has a list of required packages used in the project.

