from flask_bcrypt import Bcrypt
import pymongo

# Hash the password
bcrypt = Bcrypt()
hashed_password = bcrypt.generate_password_hash("password123").decode('utf-8')

# Connect to MongoDB
conn = "mongodb+srv://atharvarajpurkar03:athu9184@cluster1.kx71t.mongodb.net/?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true"
client = pymongo.MongoClient(conn)
db = client.db

# Insert a new user
db.users.insert_one({"email": "test@example.com", "password": hashed_password})

print("User added successfully!")
