# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.team_db

# Drops collection if available to remove duplicates
db.team.drop()

print("\nAttempting to load data...")
# Creates a collection in the database and inserts two documents
db.team.insert_many(
    [
        {
            'player': 'Jessica',
            'position': 'Point Guard'
        },
        {
            'player': 'Mark',
            'position': 'Center'
        }
    ]
)

if __name__ == "__main__":
    print("\nAttempting to retrieve any loaded data....")
    teams = list(db.team.find())
    print("\nOur team data is:\n")
    for team in teams:
        print(team)
    print("\nProcess Complete!\n")    

