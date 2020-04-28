from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import time
import pymongo

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

def scrape_news():
    # Variables
    top_article_title=""
    top_article_body=""
    # Return Var
    latest_news = {}

    #---------------- Scrape Latest News from Nasa--------------------#
    nasa_url = 'https://mars.nasa.gov/news'
    # with Browser('chrome', **executable_path, headless=False) as browser:
    browser.visit(nasa_url)
    time.sleep(3)
    html=browser.html

    soup = BeautifulSoup(html, 'html.parser')
    titles = soup.find('div', class_="list_text")

    top_article_title = titles.find('a')['href']
    top_article_body = titles.find('div',class_="article_teaser_body").tex

    latest_news = {'title':top_article_title,'article':top_article_body}  

    return latest_news

def save_latest_news():
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.mars_db
    db.latest_news.drop()
    print("\nAttempting to load data...")
    db.latest_news.insert_one(scrape_news())   
    print("Success load into database")

def scrape_feature_image():
    # Variables
    feat_img_url = "" 
    feat_img_url_1 = ""
    # Return Var
    feat_img_url_2 = "" 

    #---------------- Scrape feature Image from JPL--------------------#
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    browser.visit(jpl_url)
    html = browser.html
    time.sleep(3)

    soup = BeautifulSoup(html, 'html.parser')
    find_div_1 = soup.find('div', class_="jpl_logo")
    feat_img_url_1 = find_div_1.a['href']

    feat_img_url_1='http:'+feat_img_url_1

    find_div_raw = soup.find('li', class_="slide")
    feat_img_url = find_div_raw.a['data-fancybox-href']
    # Get url for the mars latest image
    feat_img_url_2=feat_img_url_1+feat_img_url[1:]
    feature_image = {'feat_image':feat_img_url_2}

    return feature_image

def save_feature_image():
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.mars_db
    db.feature_image.drop()
    print("\nAttempting to load data...")
    db.feature_image.insert_one(scrape_feature_image())
    print("Success load into database")

def scrape_weather():
    # Return Var
    mars_weather = ""

    #---------------- Scrape Weather from Twitter --------------------#
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    extract_mars_weather = soup.find_all('div', attrs={'data-testid':'tweet'})
    for each_weather in extract_mars_weather:
        print(each_weather)
        mars_weather_info = each_weather.find_all('span')[4].list_text
        break

    mars_weather = {"mars_weather":mars_weather_info}
    return mars_weather

def save_weather():
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.mars_db
    db.weather.drop()
    print("\nAttempting to load data...")
    db.weather.insert_one(scrape_weather())
    print("Success load into database")


def get_latest_news():
    conn = 'mongodb://localhost:27017'
    # Pass connection to the pymongo instance.
    client = pymongo.MongoClient(conn)
    # Connect to a database. Will create one if not already available.
    db = client.mars_db
    mars_latest_news = db.latest_news.find()
    return mars_latest_news



    




