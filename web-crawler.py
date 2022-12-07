
import mechanicalsoup
import sqlite3
import pandas as pd

browser = mechanicalsoup.StatefulBrowser()
browser.open("https://en.wikipedia.org/wiki/Rome")

#extract tables
th = browser.page.find_all("th", attrs={"class": "table-rh}"})
disribution = [value.txt for value in th]
print(disribution)