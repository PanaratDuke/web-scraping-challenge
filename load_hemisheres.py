# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo
import mars_hemispheres

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db

# Drops collection if available to remove duplicates
db.hemispheres.drop()
db.team.drop()

print("\nAttempting to load data...")
# Creates a collection in the database and inserts two documents

# db.replace({}, mars_hemispheres.hemisphere_image_urls, upsert=True)
db.hemisheres.insert_many([mars_hemispheres.hemisphere_image_urls])

if __name__ == "__main__":
    # print("\nAttempting to retrieve any loaded data....")
    # hemisheres = list(db.hemispheres.find())
    # print("\nOur team data is:\n")
    # for each_hem in hemispheres:
    #     print(hemisheres)
    # print("\nProcess Complete!\n")    

