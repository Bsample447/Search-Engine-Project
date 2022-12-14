import os
from modules import db, crawler      #imports database and web crawler
from threading import Thread

new_thread = Thread(target=web_crawl()) #creates web_crawl as a thread

new_thread.start()                      #starts web_crawl

db = db.Database()                      #db assignment


def clr():                              #clearing function 
    clr = os.system('clear')
    return clr




def user_menu():                        #first user menu
    option = input("""
What would you like to do?
    1.) New Search
    2.) Exit
""")
    if option == "1":
        clr()
        search_input()
    elif option == "2":
        exit()
    else:
        input("""
    Enter a number between 1 and 2.
""")
        clr()
        return user_menu()




    
            




def search_input():                  #passes db.py user input keyword
    print("'This passes key word(s) to db.py'")
    keyword = str(input(f"Type the key word(s) you would like to search for. \n")).lower()
    search_db(keyword)

def search_db(keyword):
    if keyword == "mountain":
        print("you typed mountain")
    else:
        run_crawler(keyword)


def run_crawler(keyword):                  #will run the crawler with user input
    print(keyword)





if __name__ == "__main__":
    user_menu()

