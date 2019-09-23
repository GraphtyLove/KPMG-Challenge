from pymongo import MongoClient

# MongoDB connection info
databaseName = 'kpmg'

# Connect to server
client = MongoClient("mongodb://user:user@54.37.157.250:27017/admin")
# Select a collection
db = client['admin']
dbcol = db['test2']

my_json = {
        "name": "Maxim"
        }


dbcol.insert_one(my_json)


# Print output
print(db.list_collection_names())

for i in dbcol.find():
    print(i)




db.createUser(
  {
    user: "root",
    pwd: "root"
    roles: [ { role: "userAdminAnyDatabase", db: "admin" }, "readWriteAnyDatabase" ]
  }
)