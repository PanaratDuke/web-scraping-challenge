# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo
import mars_space_img

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db

# Drops collection if available to remove duplicates
db.space_img.drop()

print("\nAttempting to load data...")
# Creates a collection in the database and inserts two documents

# db.replace({}, mars_hemispheres.hemisphere_image_urls, upsert=True)
db.mars_space_img.insert_many([mars_space_img.feat_img_dict])


