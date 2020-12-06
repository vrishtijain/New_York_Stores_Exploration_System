#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np


# In[3]:


def preprocess():


    liquor = pd.read_csv(
        "./code/datasets/Liquor_Authority_Current_List_of_Active_Licenses.csv", low_memory=False)


    # In[4]:


    liquor.head()


    # In[5]:


    authorised_liquor_store = liquor[['Serial Number', 'License Type Code', 'License Class Code', 'Certificate Number', 'Premise Name', 'DBA', 'License Issued Date', 'License Expiration Date', 'Method of Operation'
                                    ]]


    # In[6]:


    liquor['Premise Address 2'].unique()


    # In[7]:


    liquor_address = liquor[['Serial Number', 'Premise Address',
                            'Premise City', 'Premise State', 'Premise Zip', 'Georeference']]


    # In[8]:


    liquor_county_zip = liquor[['Premise Zip', 'County']]


    # In[ ]:


    # In[9]:


    farmers = pd.read_csv(
        "./code/datasets/Farmers__Markets_in_New_York_State.csv", low_memory=False)
    farmers.head()


   


    farmers_market = farmers[['Market Name', 'Address Line 1', 'City', 'Zip', 'Contact', 'State', 'Phone', 'Market Link', 'Operation Hours', 'Operation Season',
                            'Operating Months', 'FMNP', 'SNAP', 'FCC Issued', 'FCC Accepted', 'Latitude', 'Longitude']]


    farmer_county_zip = farmers[['Zip', 'County']]




    retail = pd.read_csv(
        "./code/datasets/Retail_Food_Stores.csv")
    
   




    retail_food_stores = retail[['License Number', 'Establishment Type', 'Entity Name',
                                'DBA Name', 'Street Number', 'Street Name', 'City',
                                'State', 'Operation Type', 'Zip Code', 'Square Footage']]

  


    retail_county_zip = retail[['Zip Code', 'County']]


  
  

    state_zip = pd.read_csv(
        "./code/datasets/New_York_State_ZIP_Codes-County_FIPS_Cross-Reference.csv", low_memory=False)


 

    new_york_state_zip_code = state_zip[[
        'State FIPS', 'County Code', 'ZIP Code', 'File Date']]


    state_zip.head()




    county_name_code = state_zip[['County Name', 'County Code']]


 

    county_zip = state_zip[['ZIP Code', 'County Name']]


    
    county_zip.columns = ['zip', 'county']
    retail_county_zip.columns = ['zip', 'county']
    farmer_county_zip.columns = ['zip', 'county']
    liquor_county_zip.columns = ['zip', 'county']


    


    frames = [county_zip, retail_county_zip, farmer_county_zip, liquor_county_zip]

    global_county_zip_code = pd.concat(frames)
  
   
    global_county_zip_code.shape

    global_county_zip_code = global_county_zip_code.drop_duplicates(subset='zip')


    


    

    
    global_county_zip_code.to_csv('./code/datasets/global_county_zip_code.csv')
    county_name_code.to_csv('./code/datasets/county_name_code.csv')
    retail_food_stores.to_csv('./code/datasets/retail_food_stores_short.csv')
    authorised_liquor_store.to_csv('./code/datasets/authorised_liquor_store.csv')
    liquor_address.to_csv('./code/datasets/liquor_address.csv')
    farmers_market.to_csv('./code/datasets/farmers_market.csv')
    new_york_state_zip_code.to_csv('./code/datasets/new_york_state_zip_code.csv')
    
   



   


#%%
