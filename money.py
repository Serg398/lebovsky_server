from pymongo import MongoClient


cluster = MongoClient("mongodb://127.0.0.1", 27017)
# Кластер
db = cluster["lebovsky"]
# Коллекции
usersCol = db["users"]
eventCol = db["events"]
idCol = db["id"]
profileCol = db["profile"]


def editsumm(email1, email2, oldmoney, newmoney):
    user1 = profileCol.find({"email": f"{email1}"})
    print(user1)
    users1money = int(list(user1)[0]["money"])
    user2 = profileCol.find({"email": f"{email2}"})
    users2money = int(list(user2)[0]["money"])
    profileCol.update_one({"email": f"{email1}"}, {'$set': {'money': users1money - oldmoney}})
    profileCol.update_one({"email": f"{email2}"}, {'$set': {'money': users2money + oldmoney}})
    user1 = profileCol.find({"email": f"{email1}"})
    users1money = int(list(user1)[0]["money"])
    user2 = profileCol.find({"email": f"{email2}"})
    users2money = int(list(user2)[0]["money"])
    profileCol.update_one({"email": f"{email1}"}, {'$set': {'money': users1money + newmoney}})
    profileCol.update_one({"email": f"{email2}"}, {'$set': {'money': users2money - newmoney}})
    return True