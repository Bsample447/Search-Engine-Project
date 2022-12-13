import os
#from modules import db.py               #imports database

def clr():                              #clearing function 
    clr = os.system('clear')
    return clr

#db = db.Database()                      #db assignment



def user_menu():                        #first user menu
    option = input("""
What would you like to do?
    1.) New Search
    2.) Something Else
    3.) Another Thing
    4.) Exit
""")
    if option == "1":
        clr()
        search_input()
    elif option == "2":
        pass
    elif option == "3":
        pass
    elif option == "4":
        exit()
    else:
        input("""
    Enter a number between 1 and 4.
""")
        clr()
        return user_menu()




    
            




def search_input():                  #searches db.py for a specific keyword
    print("'This searches db.py for key word(s)'")
    keyword = str(input(f"Type the key word(s) you would like to search for. \n")).lower()
    search_db(keyword)
    #    pass                        #if keyword matches what is in db, pull the db file.
    #else:
    #    run_crawler()               #if keyword has no matches, run the crawler for the keyword

def search_db(keyword):
    if keyword == "mountain":
        pass
    else:
        run_crawler(keyword)

def run_crawler(keyword):                  #will run the crawler with user input
    print(keyword)





if __name__ == "__main__":
    user_menu()

