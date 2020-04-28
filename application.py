from flask import Flask, render_template
import pymongo
import mars_scraping

# Create an instance of our Flask app.
app = Flask(__name__)

# Set up Mongo
mongo_conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(mongo_conn)
db=client.mars_db

# Set route
@app.route('/')
def index():
    try:
        news = mars_scraping.get_results()
        feature_img = mars_scraping.get_results()
    except:
        scrape()
        news = mars_scraping.get_results()
        feature_img = mars_scraping.get_results()

    return render_template(
        'index.html', 
        news=news,
        mars_img_url=feature_img)

@app.route('/scrape')
def scrape():
    mars_scraping.scrape_and_save_mars()
    

if __name__ == "__main__":
    app.run(debug=True)
