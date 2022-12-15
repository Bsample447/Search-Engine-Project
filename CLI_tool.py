import os
from modules import db                  #imports database
import crawler                          #imports everything from crawler.py
from threading import Thread            #threading
import time                             #time for threading

###############################################################################
#                               Functions                                     #
###############################################################################

def clr():                              #clearing function 
    clr = os.system('clear')
    return clr

def user_menu():                        #first user menu
    #clr()
    option = input("""What would you like to do?
    1.) New Search
    2.) List Keywords
    3.) List URLs
    4.) Exit
""")
    if option == "1":
        #clr()
        search_input()

    elif option == "2":
        result = str(db.show_list("keywords"))
        print("Total Number of Keywords in Database:", result)
        print()
        user_menu()

    elif option == "3":
        result = str(db.show_list("urls"))
        print("Total Number of URLs in Database:", result)
        print()
        user_menu()
    
    elif option == "4":
        quit = str.lower(input("""Are you sure you want to quit?
(Type 'yes' to quit)\n"""))
        if quit == "yes":
            exit()
        else:
            #clr()
            return user_menu()
    else:
        #clr()
        input("""Enter a number between 1 and 2.
Press any key to continue.
""")
        #clr()
        return user_menu()

def search_input():                  #passes db.py user input keyword
    search_input = str.lower(input(f"Type the key word(s) you would like to search for. \n"))
    keyword = search_input.split()
    result = db.search(keyword)
    #clr()
    print("Here are your search results:\n")
    for i in result:
        print(i)
    print()
    user_menu()

###############################################################################
#                               Main                                          #
###############################################################################

if __name__ == "__main__":
    db = db.Database()
    db.create_schema()
    new_thread = Thread(target=crawler.web_crawl)      #creates web_crawl
    new_thread.daemon = True
    new_thread.start()                                  #starts web_crawl
    user_menu()




