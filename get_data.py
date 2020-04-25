
# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create connection variable
mongo_conn = 'mongodb://localhost:27017'

def get_teams():
    # Pass connection to the pymongo instance.
    client = pymongo.MongoClient(mongo_conn)
    # Connect to a database. Will create one if not already available.
    db = client.team_db
    return list(db.team.find())
    
# This line is for training purposes only, you would not normally put this in code.
print(f"\nHey There, I'm the get data code.  My name is {__name__}")

if __name__ == "__main__":
    print("\nTesting Data Retrieval:....\n")
    teams = get_teams()
    for player in teams:
        print(player)
    print("\nProcess Complete!\n")    














