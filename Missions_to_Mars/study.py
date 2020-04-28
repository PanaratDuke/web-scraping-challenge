# Imports
from bs4 import BeautifulSoup as bs
import json
import pandas as pd
import pymongo
import requests
from splinter import Browser

CHROMEDRIVER_FULL_PATH = 'C:/Users/norma/Anaconda3/chromedriver.exe'
CONN_MONGO = 'mongodb://localhost:27017'

class MarsInfo:
    _URL_NASA_MARS = 'https://mars.nasa.gov/news/'
    _URL_JPL_SPACE_IMAGES = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    _URL_MARS_WEATHER = 'http://twitter.com/marswxreport?lang=en'
    _URL_MARS_FACTS = 'https://space-facts.com/mars/'
    _URL_MARS_HEMISPHERE_IMAGES = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


    def __init__(self):
        pass

    def retrieve(self):
        mongo_client = pymongo.MongoClient(CONN_MONGO)
        self.mars_db = mongo_client.MarsDB
        return {'News' : self.mars_db.News.find_one({}, {'_id':False}),
                'Image' : self.mars_db.Image.find_one({}, {'_id':False}),
                'Weather' : self.mars_db.Weather.find_one({}, {'_id':False}),
                'Facts' : self.mars_db.Facts.find_one({}, {'_id':False}),
                'Hemispheres' : self.mars_db.Hemispheres.find_one({}, {'_id':False})
               }

    def update_news(self):
        # Retrieve NASA Mars News
        try:
            soup = bs(requests.get(self._URL_NASA_MARS).content, 'html.parser')
            first_article = soup.find('li', class_ = 'slide')
            nasa_title = first_article.find('h3').text.strip()
            nasa_abstract = first_article.find('div', class_ = 'article_teaser_body').text.strip()

        except Exception as ex:
            print('Failed to update News.','\n',ex)
            #raise ex

        else:
            self.mars_db.News.drop()
            self.mars_db.News.insert_one({'title':nasa_title,'abstract':nasa_abstract})
            print('Successfully updated News')

    def update_image(self):
        # Retrieve Featured Mars Image from JPL
        try:
            self.browser.visit(self._URL_JPL_SPACE_IMAGES)
            self.browser.links.find_by_partial_text('FULL IMAGE').click()
            self.browser.links.find_by_partial_text('more info').click()
            soup = bs(self.browser.html, 'html.parser')
            featured_image_url = 'https://www.jpl.nasa.gov' + soup.find('figure').find('a')['href']

        except Exception as ex:
            print('Failed to update Image.','\n',ex)
            #raise ex

        else:
            self.mars_db.Image.drop()
            self.mars_db.Image.insert_one({'url':featured_image_url})
            print('Successfully updated Image')

    def update_weather(self):
        # Retrieve Mars Weather
        try:
            soup = bs(requests.get(self._URL_MARS_WEATHER).content, 'html.parser')
            mars_weather=soup.find('p', class_='TweetTextSize').text.strip()

        except Exception as ex:
            print('Failed to update Weather.','\n',ex)
            #raise ex

        else:
            self.mars_db.Weather.drop()
            self.mars_db.Weather.insert_one({'conditions':mars_weather})
            print('Successfully updated Weather')

    def update_facts(self):
        # Retrieve Mars Facts
        try:
            dfs = pd.read_html(self._URL_MARS_FACTS)
            df_mars_facts = dfs[0]
            df_mars_facts.columns = ['Attribute','Value']
            table_html = df_mars_facts.to_html(index=False, justify='center', classes=['table','table-sm','table-striped'])

        except Exception as ex:
            print('Failed to update Facts.','\n',ex)
            #raise ex

        else:
            self.mars_db.Facts.drop()
            self.mars_db.Facts.insert_one({'table_html':table_html})
            print('Successfully updated Facts')

    def update_hemispheres(self):
        # Retrieve Images for the Mars Hemispheres
        try:
            self.browser.visit(self._URL_MARS_HEMISPHERE_IMAGES)
            soup = bs(self.browser.html, 'html.parser')
            hemisphere_image_urls = list()
            for div in soup.find_all('div', class_='description'):
                key_word = div.find('h3').text
                self.browser.links.find_by_partial_text(key_word).click()
                soup2 = bs(self.browser.html,'html.parser')
                downloads = soup2.find('div', class_='downloads')
                img_url = downloads.find('a')['href']
                hemisphere_image_urls.append({'title':key_word.replace(' Enhanced',''),'img_url':img_url})
                self.browser.back()

        except Exception as ex:
            print('Failed to update Hemispheres.','\n',ex)
            #raise ex

        else:
            self.mars_db.Hemispheres.drop()
            self.mars_db.Hemispheres.insert_one({'title_and_image_list':hemisphere_image_urls})
            print('Successfully updated Hemispheres.')

    def update(self):
        # Initialize a headless browser
        self.browser = Browser('chrome', CHROMEDRIVER_FULL_PATH, headless=True)

        # Connect to the Mongo DB
        mongo_client = pymongo.MongoClient(CONN_MONGO)
        self.mars_db = mongo_client.MarsDB        

        # Attempt to rescrape each of the five target sites
        self.update_news()
        self.update_image()
        self.update_weather()
        self.update_facts()
        # Skip this slow update of the four hemisphere images; these images don't change
        # self.update_hemispheres()