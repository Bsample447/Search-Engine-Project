#Wikipedia Crawler V2.0 (inserting results into MySQL)
# For Embry riddle Applied Information Technology Skillbridge project, by: Brandon Saple, Chris Light, Terry Miller, and Reggie Ware 

import sqlite3
import time    
import urllib.request    #Extracting web pages
import re
import db

db = db.Database()



#Defining pages
#starting_list = ["https://en.wikipedia.org/wiki/Roman_Empire"]
#starting_list += db.crawled()
#starting_page = starting_list[-1]
seed_page = "https://en.wikipedia.org"  #Crawling English side of Wikipedia


#Downloading entire Web Document (Raw Page Content)
def download_page(url):
    try:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib.request.Request(url, headers = headers, method="HEAD")
        resp = urllib.request.urlopen(req)

        if "text/html" in resp.getheader('content-type'):
            req = urllib.request.Request(url, headers = headers, method="GET")
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        else:
            return None
    except Exception as e:
        print(str(e))


#Extract the title tag
def extract_title(page):
    start_title = page.find("<span dir")
    end_start_title = page.find(">",start_title+1)
    stop_title = page.find("</span>", end_start_title + 1)
    title = page[end_start_title + 1 : stop_title]
    return title

#####################################################################
#Extract the see also section elements
def extract_see_also(page):
    if 'id="See_also">' in page:
        start_see_also = page.find('id="See_also">')
        start_list_items = page.find('<li>', start_see_also + 1)
        end_see_also = page.find('<h2>', start_list_items + 1)
        see_also_section = page[start_list_items: end_see_also]
        pure_item_raw = (re.sub(r'<.+?>', '', see_also_section)).replace('\n', ',')
        pure_item_raw2 = pure_item_raw.replace(',,', ',')
        pure_item = pure_item_raw2.replace(',,', ',')
        flag = 0
    else:
        pure_item = "No Related Links"
        flag = 1
    return pure_item, flag

#Extract just the Introduction part of the page
def extract_introduction(page):
    start_introduction = page.find("<p>")
    stop_introduction = page.find('<div id="toctitle">', start_introduction + 1)
    
    #If the page onl has introduction
    if '<div id="toctitle">' not in page:
        stop_introduction = page.find('</p>', start_introduction + 1)
    else:
        pass
    
    
    raw_introduction = page[start_introduction : stop_introduction]
    return raw_introduction


#Extract all the links
#Finding 'Next Link' on a given web page
def get_next_link(s):
    start_link = s.find("<a href")
    if start_link == -1:    #If no links are found then give an error
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_quote = s.find('"', start_link)
        end_quote = s.find('"',start_quote+1)
        link = str(s[start_quote+1:end_quote])
        return link, end_quote
          
#Getting all links with the help of 'get_next_links'
def get_all_links(page):
    links = []
    while True:
        link, end_link = get_next_link(page)
        if link == "no_links":
            break
        else:
            if link.startswith("/") or link.startswith(seed_page):
                links.append(link)      #Append all the links in the list named 'Links'
            #time.sleep(0.1)
            page = page[end_link:]
    return links 


#Remove all the HTML tags from the introduction to get the pure text
#Eliminate all the text inside '<' & '>'
def extract_pure_introduction(page):
    pure_introduction = (re.sub(r'<.+?>', '', page)) 
    return pure_introduction

#Crawl Initiation
#Check for file type in URL so crawler does not crawl images and text files
def extension_scan(url):
    a = ['.png','.jpg','.jpeg','.gif','.tif','.txt']
    j = 0
    while j < (len(a)):
        if a[j] in url:
            #print("There!")
            flag2 = 1
            break
        else:
            #print("Not There!")
            flag2 = 0
            j = j+1
    #print(flag2)
    return flag2


#URL parsing for incomplete or duplicate URLs
def url_parse(url):
    try:
        from urllib.parse import urlparse
    except ImportError:
        from urlparse import urlparse
    url = url  #.lower()    #Make it lower case
    s = urlparse(url)       #parse the given url
    seed_page_n = seed_page #.lower()       #Make it lower case
    #t = urlparse(seed_page_n)     #parse the seed page (reference page)
    i = 0
    flag = 0

    while i<=9:
        if url == "/":
            url = seed_page_n
            flag = 0  
        elif "#" in url:
            url = url[:url.find("#")]
            flag = 0
        elif "?" in url:
            url = url[:url.find("?")]
            flag = 0
        elif s.netloc == "":
            url = seed_page + s.path
            flag = 0
        elif not s.scheme:
            url = "http://" + url.lstrip('/')
            flag = 0
        elif ".ogg" in url:
            flag = 1
        elif "upload." in url:
            flag = 1
        elif "Help:IPA" in url:
            flag = 1
        elif "%" in url:
            flag = 1
        #elif "www" not in url:
        #    url = "www."[:7] + url[7:]
        #    flag = 0
            
        elif url[len(url)-1] == "/":
            url = url[:-1]
            flag = 0
        #elif s.netloc != t.netloc:
        #    url = url
        #    flag = 1
        #    break        
        else:
            url = url
            flag = 0
            break
        
        i = i+1
        s = urlparse(url)   #Parse after every loop to update the values of url parameters

    flag2 = extension_scan(url)

    if flag == 1 or flag2 == 1:
        return None
    else:
        return url
     
t0 = time.time()
database = {}   #Create a dictionary

def getKeyword(url):
    url = url.lower()

    def validWord(w):
        blacklist = ["the", "and"] 

        return len(w) >= 3 and w not in blacklist

    return list(filter(validWord, url.split('/')[-1].split('_')))


#Main Crawl function that calls all the above function and crawls the entire site sequentially
def web_crawl():
    starting_list = ["https://en.wikipedia.org/wiki/Roman_Empire"]
    starting_list += db.crawled()
    starting_page = starting_list[-1]  

    db.remember([starting_page])
    
    crawled=[]      #Define list name 'Seed Page'
    #database = {}   #Create a dictionary

    linksCrawled = 0

    while True:
        urlLink = db.nextUrl()     #If there are elements in to_crawl then pop out the first element

        if urlLink == "None":
            #print("Out of links")
            break

        #print("Link = " + urlLink)
        #print()
        keyword = getKeyword(urlLink) 
        #print("Keywords for link:", keyword)
        #print()

        raw_html = download_page(urlLink)
        #print(raw_html)

        if raw_html == None: continue

        title_upper = str(extract_title(raw_html))
        title = title_upper.lower()     #Lower title to match user queries
        #print("Title = " + title)
        
        
        see_also,flag2 = extract_see_also(raw_html)
        #print("Related Links = " + see_also)
        
        
        raw_introduction = extract_introduction(raw_html)
        #print("Raw Introduction = " + raw_introduction)
        
        all_links = get_all_links(raw_introduction)
        all_links = filter(None, map(url_parse, all_links))
        db.remember(all_links)

        crawled.append(urlLink)
        
        #pure_introduction = extract_pure_introduction(raw_introduction)
        #print("Introduction = " + pure_introduction.replace('   ',' '))        ================  Paused printing of intro section
        
        #database [title] = pure_introduction        #Add title and its introduction to the dict
        
        #Writing the output data into a text file
        #file = open('database.txt', 'a')        #Open the text file called database.txt
        #file.write(title + ": " + "\n")         #Write the title of the page
        #file.write(pure_introduction + "\n\n")      #write the introduction of that page
        #file.write() #
        #file.close()                            #Close the file
        

        #Remove duplicated from to_crawl
        # n = 1
        # j = 0

        # while j < (len(to_crawl)-n):
        #     if to_crawl[j] in to_crawl[j+1:(len(to_crawl)-1)]:
        #         to_crawl.pop(j)
        #         n = n+1
        #     else:
        #         pass     #Do Nothing
        #     j = j+1

        linksCrawled = db.linksCrawled()
        knownURLs = db.knownURLs()
        remaining = knownURLs - linksCrawled

        #print("Total links crawled")
        #print(linksCrawled)
        #print()
        #print("Links left to crawl")
        #print(remaining)
        #print()
        #print("========== Next page ==========")

        db.add(urlLink, keyword)

        #print(to_crawl)
        #print("Iteration No. = " + str(i))
        #print("To Crawl = " + str(len(to_crawl)))
        #print("Crawled = " + str(len(crawled)))

    return ""




if __name__ == "__main__":
    db.create_schema()
    web_crawl()
    #print()

    


t1 = time.time()
total_time = t1-t0
#print(total_time)