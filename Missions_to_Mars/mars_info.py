from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import time
import pymongo

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

def scrape_mars():

    nasa_url = 'https://mars.nasa.gov/news'

    news_header = ""
    news_body = ""

    browser.visit(nasa_url,'html.parser')
    time.sleep(3)
    html=browser.html
    try:
        soup = BeautifulSoup(html, 'html.parser')
        nasa_news = soup.find('li', class_="slide")
        news_header = nasa_news.find('h3').text.strip()
        news_body = nasa_news.find('div', class_='article_teaser_body').text.strip()
        results = {'news_header':news_header,'news_body': news_body}
        print(results)
    except Exception as ex:
        print ('Failed to retreive the latest news', '\n',ex)
    


