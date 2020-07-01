import os
from pymongo import MongoClient
import urllib.parse
import json
import csv
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re

# ===========================================
# Connect to MongoDB Atlas
username = urllib.parse.quote_plus('mongo')
password = urllib.parse.quote_plus('mongo')
client = MongoClient(
    'mongodb+srv://%s:%s@cluster0-8yire.mongodb.net/test?retryWrites=true&w=majority' % (username, password))


# Create local "art" database on the fly from API call
db = client["art"]
art_data = {}


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    # =================================================================================
    # getting art facts
    # =================================================================================

    browser = init_browser()

    url = 'https://en.wikipedia.org/wiki/List_of_most_expensive_paintings'
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    # print(soup)

    #  Collecting info from the Wikipedia page
    title = soup.find('h1', class_='firstHeading').text
    print(title)

    header = soup.find(id='Background')
    p = header.find_next('p').text
    print(p)
    tables = pd.read_html(url)
    # # print(tables[0])

    table_df = tables[0]
    art_table_html = table_df.to_html(index=False, header=False)

    art_data['table'] = art_table_html

    art_data['title'] = title
    art_data['p'] = p
    # art_data['url'] = url

    # print(art_data)
    # Return results
    return art_data


art_data = scrape_info()
# Create collections on the fly
db["art"].insert_one(art_data)
