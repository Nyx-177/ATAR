import requests
import sqlite3

# create a new database
conn = sqlite3.connect('data.sqlite')
cur = conn.cursor()