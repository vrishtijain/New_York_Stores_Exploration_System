from csv import DictReader
import csv
import pandas as pd
import math
import psycopg2
from sqlalchemy import create_engine
from pymongo import MongoClient
import json
# connection = psycopg2.connect(user = "plantadmin",
#                                 password = "theadminoftheplant",
#                                 host = "127.0.0.1",
#                                 port = "5432",
#                                 database = "powerplant")
engine = create_engine('postgresql+psycopg2://project:project@127.0.0.1:5432/project')


def convertToInt(d):

    return int(float(d))

g_county_zip = pd.read_csv('./data/preprocessed/global_county_zip_code.csv')


g_county_zip = g_county_zip.dropna(subset=['zip'])
#
g_county_zip = g_county_zip[g_county_zip.zip.apply(lambda x: x.isnumeric())]
g_county_zip = g_county_zip.dropna(subset=['zip'])
g_county_zip['zip'] = g_county_zip['zip'].astype(str).astype(int)
g_county_zip = g_county_zip[g_county_zip['zip'] < 100000]
g_county_zip = g_county_zip.drop_duplicates(subset='zip', keep="first")
g_county_zip = g_county_zip[['zip', 'county']]

# INSERTTT
g_county_zip = g_county_zip.set_index('zip', drop=True)
#g_county_zip.to_sql('global_county_zip_code', engine, if_exists='append')


# retail_food_stores
r_food = pd.read_csv('./data/preprocessed/retail_food_stores.csv')

r_food = r_food.set_index('License Number', drop=True)

r_food.columns = ['license', 'establishment_type',
                  'entity_name', 'dba_name', 'street_number', 'street_name', 'city', 'state', 'operation_type', 'zip_code', 'square_footage']
# drop if primary key is na
r_food = r_food.dropna(subset=['license'])
r_food = r_food.drop_duplicates(subset='license', keep="first")

# convcert to integer columns
r_food['zip_code'] = r_food['zip_code'].astype(str).astype(int)
r_food = r_food[r_food['zip_code'] < 100000]
r_food['square_footage'] = r_food['square_footage'].astype(str).astype(int)
r_food = r_food.set_index('license', drop=True)

# INSERTTT
#r_food.to_sql('retail_food_stores', engine, if_exists='append')



# authorised_liquor_store
liquor_store = pd.read_csv('./data/preprocessed/authorised_liquor_store.csv')

liquor_store = liquor_store.iloc[:, 1:]


liquor_store.columns = ['serial_number', 'license_type_code',
                        'license_class_code', 'certificate_number', 'premise_name', 'dba', 'license_issued_date', 'license_expiration_date', 'method_of_operation']


# drop if primary key is na
liquor_store = liquor_store.dropna(subset=['serial_number'])
liquor_store = liquor_store.drop_duplicates(subset='serial_number', keep="first")

one_m8 = list(liquor_store['serial_number'][liquor_store['license_class_code'] == '1M8'])

# print(one_m8)

# convcert to integer columns
liquor_store = liquor_store[liquor_store.license_class_code.apply(lambda x: x.isnumeric())]
liquor_store['serial_number'] = liquor_store['serial_number'].astype(str).astype(int)
liquor_store['license_class_code'] = liquor_store['license_class_code'].astype(str).astype(int)
liquor_store['certificate_number'] = liquor_store['certificate_number'].astype(str).astype(int)
liquor_store = liquor_store.set_index('serial_number', drop=True)


# INSERTTT
#liquor_store.to_sql('authorised_liquor_store', engine, if_exists='append')




# liquor_store
liquor_address = pd.read_csv('./data/preprocessed/liquor_address.csv')

liquor_address = liquor_address.iloc[:, 1:]


liquor_address.columns = ['serial_number', 'premise_address',
                        'city', 'state', 'premise_zip_code', 'georeferences' ]
# drop if primary key is na
liquor_address = liquor_address.dropna(subset=['serial_number'])
liquor_address = liquor_address.drop_duplicates(subset='serial_number', keep="first")


# convcert to integer columns

liquor_address['serial_number'] = liquor_address['serial_number'].astype(str).astype(int)
liquor_address = liquor_address[liquor_address.premise_zip_code.apply(lambda x: x.isnumeric())]
liquor_address['premise_zip_code'] = liquor_address['premise_zip_code'].astype(str).astype(int)
liquor_address = liquor_address[liquor_address['premise_zip_code'] < 100000]

# REMOVING 2500828 BECUASE THAT HAD STUPID VALUE 
liquor_address = liquor_address[~liquor_address['serial_number'].isin(one_m8)]
# liquor_address = liquor_address[liquor_address['serial_number'] not in one_m8]
liquor_address = liquor_address.set_index('serial_number', drop=True)
# INSERTTT
#liquor_address.to_sql('liquor_address', engine, if_exists='append')



# farmers_market
farmers_market = pd.read_csv('./data/preprocessed/farmers_market.csv')
# print(farmers_market.columns)
farmers_market = farmers_market.iloc[:, 1:]
farmers_market.columns = ['market_name', 'address_line1',
                          'city', 'zip', 'contact', 'state', 'phone', 'marklet_link', 'operation_hours',
                          'operation_season', 'operation_month', 'fnmp', 'snap', 'fcc_issued', 'fcc_accepted', 'latitude',  'longitude']


# drop if primary key is na
farmers_market = farmers_market.dropna(subset=['market_name'])
farmers_market = farmers_market.drop_duplicates(subset='market_name', keep="first")

# convcert to integer columns

farmers_market['phone'] = farmers_market['phone'].astype(str).astype(int)
farmers_market = farmers_market.dropna(subset=['zip'])
farmers_market['zip'] = farmers_market['zip'].astype(float).astype(int)
farmers_market = farmers_market[farmers_market['zip'] < 100000]

farmers_market = farmers_market.set_index('market_name', drop=True)
# INSERTTT
#farmers_market.to_sql('farmers_market', engine, if_exists='append')


# we have to do json :P


# fieldnames = ('state_fips', 'county_code', 'zip_code', 'file_date')
new_york_state_zip_code = pd.read_csv('./data/preprocessed/new_york_state_zip_code.csv',  header=0, index_col=False)


new_york_state_zip_code = new_york_state_zip_code.iloc[:, 1:]
new_york_state_zip_code.columns = ['state_fips', 'county_code',
                                   'zip_code', 'file_date']


new_york_state_zip_code.to_json("./data/preprocessed/new_york_state_zip_code.json", orient="records", date_format="epoch", double_precision=10, force_ascii=True, date_unit="ms", default_handler=None)

with open('./data/preprocessed/new_york_state_zip_code.json') as f:
    json_data = json.load(f)
client = MongoClient("mongodb://localhost:27017/")
projectDB = client["project"]
consumption_collection = projectDB["project"]
consumption_collection.insert_many(json_data)

print("Done <#")
