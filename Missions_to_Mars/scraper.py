from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import pandas as pd
import time


# def get_latest_news():
    # Using Splinter to read html
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

    # Extract From NASA Website
    # URL of page to be scraped
url = 'https://mars.nasa.gov/news'

    # Read html from website
browser.visit(url)
time.sleep(3)
    # Variables to store text from website
top_article_title =""
top_article_body = ""
nasa_news = {} # Using this variable

    # Store html in var
html = browser.html

    # Read html tags into var using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
print(f"soup = {soup}")
titles = soup.find('div', class_="list_text")

top_article_title = titles.find('a').text
top_article_body = titles.find('div',class_="article_teaser_body").text

    # traverse through the dictionary using [] and use = to set value as 
nasa_news[top_article_title] = top_article_body
print(nasa_news)
    # return nasa_news

