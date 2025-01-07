import pymongo

# MongoDB connection
conn = "mongodb+srv://atharvarajpurkar03:athu9184@cluster1.kx71t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1&connectTimeoutMS=30000"
client = pymongo.MongoClient(conn)

try:
    # Test the connection
    db = client.db
    print(db.list_collection_names())  # Prints all collections
    print("Connected to MongoDB successfully!")
except Exception as e:
    print("Error:", e)
