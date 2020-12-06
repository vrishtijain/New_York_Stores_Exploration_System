import psycopg2
import psycopg2.extras
import json
import pandas as pd
from pymongo import MongoClient
import webbrowser
from psycopg2 import sql
import geopy.distance

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
            query = sql.SQL("""select 'Total Liquor Stores' as Type,  count(l.serial_number) as Total from liquor_address l \
            where l.premise_zip_code in (Select zip from global_county_zip_code where county ilike {c1}) \
            union \
            select    'Total Retail Stores' as Type,  count(rs.license) as Total from  retail_food_stores rs \
            where rs.zip_code  in (Select zip from global_county_zip_code where county ilike {c2})\
            union \
            select  'Total Farmer Market Stores' as Type,  count(fm.market_name) as Total from farmers_market fm \
            where  fm.zip in (Select zip from global_county_zip_code where county ilike {c3}) \
             """).format(
                c1=sql.Literal(county),
                c2=sql.Literal(county),
                c3=sql.Literal(county))
           

            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # print(cursor.mogrify(query, params))
            # print(cursor.mogrify(query, params))
            cursor.execute(query)
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
            
            q1 = sql.SQL("""SELECT market_name, address_line1, city, zip, contact, marklet_link, \
                    operation_hours , operation_season from \
                     farmers_market where operation_month = {op_month} """).format(op_month=sql.Literal(op_month))
            # print(cursor.mogrify(q1))
            cursor.execute(q1)
            r1 = cursor.fetchall()
            # print(r1)
            all_list = []
            for r in r1:
                # print(r[3])
                all_list.append(r[3])

            
            # get the county_code out of the given zip code
            client = MongoClient("mongodb://localhost:27017/")
            projectDB = client["project"]
            project_collection = projectDB["project"]
            
            # client.server_info()
            results = project_collection.find({"zip_code": {"$in": all_list}})
    
            zip_county_dict ={}
            for r in results:
                zip_county_dict[r['zip_code']] = r['county_code']
           

            for i in range(len(r1)):
                row= r1[i]
                r1[i].append(zip_county_dict[row[3]])
           
            i=0
            limit = len(r1)
            ans = 0
            while i<limit and ans!= str(1) :
                
                row = r1[i]
                print(row)
                
                # market_name, address_line1, city, zip, contact, marklet_link, \
                #     operation_hours, operation_season
                printing_string = "Name of the farmer's market is {0}  and their address is {1} in {2} . They are open during {3} and following season {4}. It had the county code {5} and zip code is {6}  ".format(row[0], row[1], row[2],  row[6], row[7], row[8], row[3])
                print(printing_string)
                ans = input("Do you want to open it's link (y or n) or enter 1 to stop this loop")
                if(ans =='y'):
                    # opemn he link
                    if(row[5]!= ''):
                        webbrowser.open(row[5])
                    else:
                        print("sorry cannot open, link might be missing")
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

            query = sql.SQL("""select ls.license_type_code,  count(ls.license_type_code) \
             from  authorised_liquor_store ls \
                where ls.license_issued_date >= {iss_date} and \
                ls.license_expiration_date <= {exp_date}   \
                group by ls.license_type_code \
                having count(distinct ls.license_expiration_date) >= {dis_count}  \
                order by ls.license_type_code""").format(
                iss_date=sql.Literal(iss_date),
                exp_date=sql.Literal(exp_date),
                dis_count=sql.Literal(dis_count)
                )
            

            cursor = self.conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(query)
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
        
    def search_retail_store(self):
        try:
            cursor = self.conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
            name =input("Enter the keyword you want to search for in retail store (name) ")
            sq_foot = input("Enter minimum Sqaure Foot Area for the retail store ")

            query = sql.SQL(""" select rf.entity_name,  rf.street_number, rf.street_name, rf.city, rf.state, gl.zip \
                from retail_food_stores rf inner join  global_county_zip_code gl \
                on gl.zip=rf.zip_code\
                where rf.entity_name ilike {name} and square_footage > {sq_foot}""").format(
                name=sql.Literal("%"+name+"%"),
                sq_foot=sql.Literal(sq_foot),
            )
            

            cursor.execute(query)
            # print(cursor.mogrify(query))
            result  =cursor.fetchall()
            for r in result:
                print(" store name : ",
                      r[0].rstrip(), " Street Number: ", r[1].rstrip(), " Street Name: ", r[2].rstrip(), " City : ", r[3].rstrip(), "  State : ", r[4].rstrip(), " Zip : ", r[5])



        except Exception as e:
            print("This is the Error")
            print(str(e))
            print("There is some problem with the variables contraints. Please ask for assistance from the owner of the code")
            return

    def search_farmers_markey_closet_to_you(self):
        try:
            cursor = self.conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
            query = """SELECT fm.market_name, fm.phone, fm.latitude , fm.longitude, fm.address_line1, fm.zip, global_county_zip_code.county from  farmers_market fm inner join global_county_zip_code on fm.zip = global_county_zip_code.zip"""
            lat = input("Enter your Latitude")
            lon = input("Enter your Longitude")
            km = float(input("Enter Desired KM range"))
            cursor.execute(query)
            result = cursor.fetchall()
            all_closest =[]
            coords = (lat, lon)

            for r in result:
                coord_2 = (r[2], r[3])
                dis = geopy.distance.geodesic(coords, coord_2).km
                if(dis < km):
                    all_closest.append([r,dis ])
            
            all_closest.sort(key=lambda x: x[1])
            if(len(all_closest) >=5):
                top_five = all_closest[:5]
            else:
                top_five = all_closest
            
            for el in top_five:
                print("This is the farmers market : ", el[0][0])
                print("Phone", el[0][1])
                print("Adress", el[0][4], el[0][6], el[0][5])
                print("It is at {: .2f}  kms from you   ".format(el[1]))
                print("\n")

        except Exception as e:
            print("This is the Error")
            print(str(e))
            print("There is some problem with the variables contraints. Please ask for assistance from the owner of the code")
            return



if  __name__ == "__main__":
    # we can call function like this.
    obj = DatabaseProjectStores()
    ans = 'y'
    while(ans !='n'):
        print("Menu :)")
        print("Enter")
        print("a: To Count of all stores by County name ")
        print("b: To search retail store by name ")
        print("c: To search farmers market closest to you")
        print("d: To get information about liquor store realted to issue and expiration date")
        print("e: To add a new liquor store")
        print("f: To find Farmers market based on Operations")
        print("Enter n to Exit")
        ans = input()
        if(ans =='n'):
            break 
        elif(ans =="a"):
            obj.all_stores_count()
            
        elif(ans == "b"):
            obj.search_retail_store()
            
        elif(ans == "c"):
            obj.search_farmers_markey_closet_to_you()
            
        elif(ans == "d"):
            obj.liquor_data()
           
        elif(ans == "e"):
            obj.insert_liquor_store_data()
           
        elif(ans == "f"):
            obj.farmers_market_thing()
            
        else:
            print("Nothing Matches, Enter Again")
            
    print("Thank you . Have a good day")
            

   




