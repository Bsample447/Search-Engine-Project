import os
from modules import db                  #imports database
from crawler import *                   #imports everything from crawler.py
from threading import Thread            #threading
import time                             #time for threading




###############################################################################
#                               Functions                                     #
###############################################################################

def clr():                              #clearing function 
    clr = os.system('clear')
    return clr




def user_menu():                        #first user menu
    clr()
    option = input("""What would you like to do?
    1.) New Search
    2.) Exit
""")
    if option == "1":
        clr()
        search_input()
    elif option == "2":
        quit = str.lower(input("""Are you sure you want to quit?
(Type 'yes' to quit)\n"""))
        if quit == "yes":
            exit()
        else:
            clr()
            return user_menu()
    else:
        clr()
        input("""Enter a number between 1 and 2.
Press any key to continue.
""")
        clr()
        return user_menu()



def search_input():                  #passes db.py user input keyword
    print("'This passes key word(s) to db.py'")
    search_input = str.lower(input(f"Type the key word(s) you would like to search for. \n"))
    keyword = search_input.split()
    search_db(keyword)



def search_db(keyword):             
    if keyword == ['mountain']:
        print("you typed mountain")
    else:
        print(keyword)
        return search_db


###############################################################################
#                               Main                                          #
###############################################################################

if __name__ == "__main__":
    user_menu()
    new_thread = Thread(target=web_crawl)   #creates web_crawl
    new_thread.daemon = True
    new_thread.start()                      #starts web_crawl



