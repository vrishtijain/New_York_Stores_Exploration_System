import psycopg2
import psycopg2.extras
import json
import pandas as pd
from pymongo import MongoClient
import webbrowser

class DatabaseProjectStores():
    
    def __init__(self):
        self.conn = psycopg2.connect(user = "project",
                                password = "project",
                                host = "127.0.0.1",
                                port = "5432",
                                database = "project")
    def all_stores_count(self):
        county = input("Enter County Name")
        try:
            query = """select 'Total Liquor Stores' as Type,  count(l.serial_number) as Total from liquor_address l \
            where l.premise_zip_code in (Select zip from global_county_zip_code where county ilike %(c1)s) \
            union \
            select    'Total Retail Stores' as Type,  count(rs.license) as Total from  retail_food_stores rs \
            where rs.zip_code  in (Select zip from global_county_zip_code where county ilike %(c2)s)\
            union \
            select  'Total Farmer Market Stores' as Type,  count(fm.market_name) as Total from farmers_market fm \
            where  fm.zip in (Select zip from global_county_zip_code where county ilike %(c3)s) \
             """
            params = {
            'c1': county,
                'c2': county,
                'c3': county,
            }

            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # print(cursor.mogrify(query, params))
            # print(cursor.mogrify(query, params))
            cursor.execute(query, params)
            r = cursor.fetchall()
            # print(r)
            print("Following are the Stores in the County ", county)
            for name, count in r:
                print(name, ':', count)
            return

        except Exception as e:
            print("This is the Error")
            print(str(e))
            print("There is some problem with the variables contraints. Please ask for assistance from the owner of the code")
            return


    def  insert_liquor_store_data(self):
        
        serial_number=input("Enter Serial Number (Integer)")
        lic_type_code = input("Enter  License Type Code ( like AX , OP, FW )")
        lic_class_code = input("Enter  License Class Code ( like 122, 134, 567)")
        
        certi_num = input("Enter  Certificate Number ( Integer)")
        prem_name = input("Enter  Premise Name ")
        dba = input("Enter  DBA ")
        lic_iss_date = input("Enter  License Issued Date ( like 12/11/2018)")
        lic_exp_date = input("Enter  License Expiration Date  ( like 12/11/2018)")
        meth_of_op = input("Enter  Method of Operation")
        prem_add = input("Enter  Premise Address ")
        prem_city = input("Enter Premise City")
        prem_state = input("Enter  Premise State (LIke NY , CA, NJ)")
        prem_zip = input("Enter  Premise Zip ")
        geo = input("Enter Georeference ")

        try:
           
            cursor=self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            total =0
            auth_lq_store = """INSERT INTO authorised_liquor_store (serial_number, license_type_code,
                            license_class_code, certificate_number, premise_name, dba, license_issued_date, license_expiration_date, method_of_operation) VALUES (%s, %s, %s,%s,%s,%s,%s, %s, %s)"""
            cursor.execute(auth_lq_store, (serial_number, lic_type_code, lic_class_code,
                                           certi_num, prem_name, dba,lic_iss_date, lic_exp_date, meth_of_op))

            total = total+cursor.rowcount

            lq_add = """INSERT INTO liquor_address (serial_number, premise_address,
                            city, state, premise_zip_code, georeferences) VALUES (%s, %s, %s,%s,%s, %s)"""
            cursor.execute(lq_add, (serial_number, prem_add, prem_city,
                                    prem_state, prem_zip,  geo))
            total = total+cursor.rowcount

            if( total ==2):
                self.conn.commit()
                print("Inserted Succesfully")
            else:
                print("There is some problem with the variables")
                return 
        except Exception as e:
            print("This is the Error")
            print(str(e))
            print("There is some problem with the variables contraints. Please ask for assistance from the owner of the code")
            return 0
    
    def farmers_market_thing(self):

        
        
        try:
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            q = """SELECT distinct(operation_month) from  farmers_market"""
            cursor.execute(q)
            # r1 = cursor.fetchall()
            all_operation_month = ""
            for ( r) in cursor:
                # print(r, r[0])
                all_operation_month += " " + r[0] + ", "

            print(" Enter operation_month and it should one of the following ")
            print(all_operation_month)
            op_month = input()
            
            q1 = """SELECT market_name, address_line1, city, zip, contact, marklet_link, \
                    operation_hours , operation_season from  farmers_market where operation_month = %(op_mon)s """
            params= {
                "op_mon" : op_month}
            cursor.execute(q1, params)
            r1 = cursor.fetchall()
            all_list = []
            for r in r1:
                # print(r[3])
                all_list.append(r[3])


            # get the county_code out of the given zip code
            client = MongoClient("mongodb://localhost:27017/")
            projectDB = client["project"]
            project_collection = projectDB["project"]
            
            results = project_collection.find({"zip_code": {"$in": all_list}})
            zip_county_dict ={}
            for r in results:
                zip_county_dict[r['zip_code']] = r['county_code']
            # print(zip_county_dict[14063])

            for i in range(len(r1)):
                row= r1[i]
                r1[i].append(zip_county_dict[row[3]])
            i=0
            limit = len(r1)
            ans = 0
            while i<limit and ans!= str(1) :
                row = r1[i]
                
                # market_name, address_line1, city, zip, contact, marklet_link, \
                #     operation_hours, operation_season
                printing_string = "Name of the farmer's market is {0}  and their address is {1} in {2} . They are open during {3} and following season {4}. It had the county code {5} and zip code is {}  ".format(row[0], row[1], row[2],  row[6], row[7], row[8], row[3])
                print(printing_string)
                ans = input("Do you want to open it's link (y or n) or enter 1 to stop this loop")
                if(ans =='y'):
                    # opemn he link
                    if(row[5]!= ''):
                        webbrowser.open(row[5])
                    else:
                        print("sorry cannot open, link might be missing")

                    
                    i+=1
                else:
                    i+=1
        
        except Exception as e:
            print("This is the Error")
            print(str(e))
            print("There is some problem with the variables contraints. Please ask for assistance from the owner of the code")
            return
        
    def liquor_data(self):
        try:
            
            iss_date = input("Enter License Issue Date after ")
            exp_date = input("Enter License Expiration Date before ")
            dis_count = input("Enter Number you want per count for expiration date")

            query = """select ls.license_type_code,  count(ls.license_type_code) \
             from  authorised_liquor_store ls \
                where ls.license_issued_date >= %(iss_date)s and \
                ls.license_expiration_date <= %(exp_date)s   \
                group by ls.license_type_code \
                having count(distinct ls.license_expiration_date) >= %(dis_count)s  \
                order by ls.license_type_code"""
            params ={
                'exp_date': exp_date,
                'iss_date': iss_date,
                'dis_count': dis_count
            }
            cursor = self.conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(query, params)
            # print(cursor.mogrify(query, params))
            result = cursor.fetchall()
            # print(result)
            if(result==[]):
                print("No result found")
                exit(0)
                return
            print("Following is the list of license_type_code and their respective count of Liquor store for the issue date after {0} and expiration date before {1} for number of expiration count {2} ".format(iss_date, exp_date, dis_count))
            print(" license_type_code     Count")
         
            for r in result:
                print("        " ,
                      r[0], "           ", r[1])

        
        except Exception as e:
            print("This is the Error")
            print(str(e))
            print("There is some problem with the variables contraints. Please ask for assistance from the owner of the code")
            return
        


    

if  __name__ == "__main__":
    # we can call function like this.
    obj = DatabaseProjectStores()
    # obj.insert_liquor_store_data()
    # obj.all_stores_count()
    # obj.farmers_market_thing()
    obj.liquor_data()



