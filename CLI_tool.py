import os
from modules import db                  #imports database
from modules import crawler                         #imports everything from crawler.py
from threading import Thread            #threading


###############################################################################
#                               Functions                                     #
###############################################################################



def user_menu():                        #first user menu
    option = input("""What would you like to do?
    1.) New Search
    2.) List Total Number of Keywords
    3.) List Total Number of URLs
    4.) Exit
""")
    if option == "1":
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
            return user_menu()
    else:
        input("""Enter a number between 1 and 4.
Press any key to continue.
""")
        return user_menu()

def search_input():                  #passes db.py user input keyword
    search_input = str.lower(input("Type the key word(s) you would like to search for. \n"))
    keyword = search_input.split()
    result = db.search(keyword)
    if result == []:
        print(f"""
Sorry, no results for {search_input}.
            """)
        user_menu()
    else:
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




