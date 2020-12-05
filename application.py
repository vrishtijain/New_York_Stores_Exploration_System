import psycopg2
import psycopg2.extras
import json
from pymongo import MongoClient

class DatabaseProjectStores:
    
    def __init__(self):
        self.conn = psycopg2.connect(user = "project",
                                password = "project",
                                host = "127.0.0.1",
                                port = "5432",
                                database = "project")
    
    