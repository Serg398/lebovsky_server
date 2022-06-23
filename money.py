import json
from pymongo import MongoClient
from bson import json_util


cluster = MongoClient("localhost", 27017)
# Кластер
db = cluster["lebovsky"]
# Коллекции
usersCol = db["users"]
eventCol = db["events"]
idCol = db["id"]


def editsumm(Email1, Email2, oldmoney, newmoney):
    user1 = usersCol.find({"Email": f"{Email1}"})
    users1money = int(list(user1)[0]["money"])
    user2 = usersCol.find({"Email": f"{Email2}"})
    users2money = int(list(user2)[0]["money"])
    usersCol.update_one({"Email": f"{Email1}"}, {'$set': {'money': users1money - oldmoney}})
    usersCol.update_one({"Email": f"{Email2}"}, {'$set': {'money': users2money + oldmoney}})
    user1 = usersCol.find({"Email": f"{Email1}"})
    users1money = int(list(user1)[0]["money"])
    user2 = usersCol.find({"Email": f"{Email2}"})
    users2money = int(list(user2)[0]["money"])
    usersCol.update_one({"Email": f"{Email1}"}, {'$set': {'money': users1money + newmoney}})
    usersCol.update_one({"Email": f"{Email2}"}, {'$set': {'money': users2money - newmoney}})
    return True