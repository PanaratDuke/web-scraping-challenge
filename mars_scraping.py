from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import time
import pymongo

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

def scrape_mars():
    # Variables
    results={}

    #---------------- Latest News from Nasa
    url = 'https://mars.nasa.gov/news'
    # with Browser('chrome', **executable_path, headless=False) as browser:
    browser.visit(url)
    time.sleep(3)
    html=browser.html
    
    top_article_title=""
    top_article_body=""

    soup = BeautifulSoup(html, 'html.parser')
    titles = soup.find('div', class_="list_text")

    top_article_title = titles.find('a')['href']
    top_article_body = titles.find('div',class_="article_teaser_body").tex

    results = {'title':top_article_title,'article':top_article_body}

    #---------------- Featurn Image from JPL
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    # Variables to store text from website
    feat_img_url = "" 
    feat_img_url_1 = ""
    feat_img_url_2 = "" #Using This one to retrieve url
    # feat_img_url_new = ""
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Find image parth first part
    find_div_1 = soup.find('div', class_="jpl_logo")
    feat_img_url_1 = find_div_1.a['href']

    feat_img_url_1='http:'+feat_img_url_1
    feat_img_url_1
    # Find image parth first part
    find_div_raw = soup.find('li', class_="slide")
    feat_img_url = find_div_raw.a['data-fancybox-href']
    feat_img_url
    # Get url for the mars latest image
    feat_img_url_2=feat_img_url_1+feat_img_url[1:]
    results = {'mars_feat_img_url':feat_img_url_2}

    return results

def scrape_and_save_mars():
    conn = 'mongodb://localhost:27017'

    client = pymongo.MongoClient(conn)

    db = client.mars_db

    db.results.drop()

    print("\nAttempting to load data...")

    db.results(scrape_mars())

def get_latest_news():
    conn = 'mongodb://localhost:27017'
    # Pass connection to the pymongo instance.
    client = pymongo.MongoClient(conn)
    # Connect to a database. Will create one if not already available.
    db = client.mars_db
    mars_latest_news = db.latest_news.find()
    return mars_latest_news

def get_results():
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.mars_db
    results = db.results.find()
    return results

    




