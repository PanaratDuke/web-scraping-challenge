
# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create connection variable
mongo_conn = 'mongodb://localhost:27017'

def get_image():
    # Pass connection to the pymongo instance.
    client = pymongo.MongoClient(mongo_conn)
    # Connect to a database. Will create one if not already available.
    db = client.mars_db
    mars_img_dict = db.mars_space_img.find()
    return mars_img_dict
    
# This line is for training purposes only, you would not normally put this in code.
print(f"\nHey There, I'm the get data code.  My name is {__name__}")

if __name__ == "__main__":
    print("\nTesting Data Retrieval:....\n")
    space_image = get_image()
    for each_space_image in space_image:
        print(each_space_image)

    print("\nProcess Complete!\n")    










