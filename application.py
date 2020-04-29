from flask import Flask, render_template, redirect
import pymongo
import mars_scraping

# Create an instance of our Flask app.
app = Flask(__name__)

# Set up Mongo
# mongo_conn = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(mongo_conn)
# db=client.mars_db
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db

# Set route
@app.route('/')
def index(): 
    print('Getting Data from Mongo')
    latest_news=db.latest_news.find_one()
    mars_space_img=db.mars_space_img.find_one()
    weather=db.weather.find_one()
    facts=db.facts.find_one()
    hemispheres=db.hemis.find_one()
    
    # try:
    #     news = mars_scraping.get_mars_info()
    #     # , fimg, weat, fact, hemis
    # except:
    #     scrape()
    #     news = mars_scraping.get_mars_info()
    return render_template(
        'index.html', 
        m_news=latest_news,
        m_fimg=mars_space_img,
        m_weather=weather,
        m_fact=facts,
        m_hemis=hemispheres
        )
    

@app.route('/scrape')
def scrape():
    print('Scraping...')
    mars_scraping.scrape_all()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
