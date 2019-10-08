# import socket
# host_name = socket.gethostname()
# host_ip = socket.gethostbyname(host_name)
# print(host_name)
# print(host_ip)
from bson import ObjectId
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client["users_database"]
# users_db = db['users']
# users = users_db['users']
# users.insert_one({'name': "name", "password": "password", "is_active": False})
# print(users.find_one({'name': "name", "password": "password"}))
# print(users.find_one({'name': "name", "password": "asf"}))
# print(users.find_one({'_id': ObjectId('5d8fbea7876ecf4d6531b4d3')}))

client.db.command("dropDatabase")
db = client["users_database"]
db.users.drop()
cursor = db.users # choosing the collection you need

for document in cursor.find():
    print (document)

print(db.list_collection_names())