from flask import Flask, render_template
import pymongo
import mars_scraping

# Create an instance of our Flask app.
app = Flask(__name__)

# Set up Mongo
# mongo_conn = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(mongo_conn)
# db=client.mars_db

# Set route
@app.route('/')
def index():
    try:
        news, fimg, weat, fact, hemis = mars_scraping.get_mars_info()
    except:
        scrape()
        news, fimg, weat, fact, hemis = mars_scraping.get_mars_info()
    return render_template(
        'index.html', 
        m_news=news,
        m_fimg=fimg,
        m_weat=weat,
        m_fact=fact,
        m_hemis=hemis
        )

@app.route('/scrape')
def scrape():
    mars_scraping.scrape_news():
    mars_scraping.save_latest_news():
    mars_scraping.scrape_weather():
    mars_scraping.save_weather():
    mars_scraping.scrape_facts()
    mars_scraping.save_facts()
    mars_scraping.scrape_hemispheres()
    mars_scraping.save_hemispheres()  

if __name__ == "__main__":
    app.run(debug=True)
