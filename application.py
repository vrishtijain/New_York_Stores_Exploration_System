from database import DatabaseProjectStores

if __name__ == "__main__":
    # we can call function like this.
    obj = DatabaseProjectStores()
    ans = 'y'
    while(ans != 'n'):
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
        if(ans == 'n'):
            break
        elif(ans == "a"):
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
