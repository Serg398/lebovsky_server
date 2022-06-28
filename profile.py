import json
from pymongo import MongoClient
from bson import json_util
from money import editsumm
from werkzeug.security import generate_password_hash, check_password_hash


cluster = MongoClient("mongodb://62.3.58.53", 27017)
db = cluster["lebovsky"]
usersCol = db["users"]
eventCol = db["events"]
idCol = db["id"]
connectCol = db["userConnect"]
profileCol = db["profile"]



def newProfile(content):
    print(content)
    contentPass = content['pass']
    contentPassHash = generate_password_hash(contentPass)
    profile = {
        "name": content["name"],
        "firstname": content["firstname"],
        "passwd": contentPassHash,
        "money": 0,
        "email": content["Email"],
        "settings": [{"city": "Белгород"}],
    }
    if profileCol.insert_one(profile):
        return True



