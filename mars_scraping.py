from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import time
import pymongo
import pandas as pd

def scrape_all():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    save_latest_news(browser)
    save_feature_image(browser)
    save_weather(browser)
    save_facts(browser)
    save_hemispheres(browser)
    # browser.close()
    pass

def scrape_news(browser):
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
    first_article = soup.find('ul', class_="item_list")

    top_article_title = first_article.find('div', class_='content_title').text
    top_article_body = first_article.find('div',class_="article_teaser_body").text

    latest_news = {'title':top_article_title,'article':top_article_body}  

    return latest_news

def save_latest_news(browser):
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.mars_db
    db.latest_news.drop()
    print("\nAttempting to load data...")
    db.latest_news.insert_one(scrape_news(browser))   
    print("Success load into database")
    pass

def scrape_feature_image(browser):
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

def save_feature_image(browser):
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.mars_db
    db.feature_image.drop()
    print("\nAttempting to load data...")
    db.feature_image.insert_one(scrape_feature_image(browser))
    print("Success load into database")

def scrape_weather(browser):
    # Return Var
    mars_weather = ""

    #---------------- Scrape Weather from Twitter --------------------#
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather_info=''
    extract_mars_weather = soup.find_all('div', attrs={'data-testid':'tweet'})
    for each_weather in extract_mars_weather:
        # print(each_weather)
        mars_weather_info = each_weather.find_all('span')[4].text
        break

    mars_weather = {"mars_weather": mars_weather_info}
    return mars_weather

def save_weather(browser):
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.mars_db
    db.weather.drop()
    print("\nAttempting to load data...")
    db.weather.insert_one(scrape_weather(browser))
    print("Success load into database")

def scrape_facts(browser):
    # Return Var
    facts_dict = {}

    #---------------- Scrape Facts from Space-Facts --------------------#
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    target_table=tables[0]
    
    # for each_row in target_table.index:
    #     each_row_df=target_table.loc[each_row]
    #     facts_dict[each_row_df[0]]=each_row_df[1]

    target_table.columns=['description', 'values']
    target_table.set_index('description', inplace=True)
    facts_dict['facts']=target_table.to_html(classes='table table-striped')
    return facts_dict

def save_facts(browser):
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.mars_db
    db.facts.drop()
    print("\nAttempting to load data...")
    db.facts.insert_one(scrape_facts(browser))
    print("Success load into database")

def scrape_hemispheres(browser):
    # Variables
    img_url = ""
    titles = ""
    # Return Var
    hemispheres_image_urls ={}
    #---------------- Scrape Facts from Space-Facts --------------------#    
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(usgs_url)
    html = browser.html
    
    soup = BeautifulSoup(html, 'html.parser')
    titles = soup.find_all('div', class_="item")

    for each_title in titles: 
        key_word = each_title.find('h3').text
        print(key_word)
#     browser.find_link_by_partial_text('Hemisphere Enhanced').click()
        browser.find_link_by_partial_text(key_word).click()
        key_word=key_word.replace(' ', '_')
#     print(browser.url)
    # you can access the attribute using [href]
        img_url = browser.find_link_by_text('Sample').first['href']
#     hemisphere_image_urls.update({test.text:img_url})
        print(img_url)
        hemispheres_image_urls[key_word]=img_url
        browser.back()
    
    print(f"out side for {hemispheres_image_urls}")

    return hemispheres_image_urls
    
def save_hemispheres(browser):
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.mars_db
    db.hemis.drop()
    print("\nAttempting to load data...")
    db.hemis.insert_one(scrape_hemispheres(browser))
    print("Success load into database")






