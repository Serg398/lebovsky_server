import json
from pymongo import MongoClient
from bson import json_util
from money import editsumm


cluster = MongoClient("mongodb://127.0.0.1", 27017)
db = cluster["lebovsky"]
usersCol = db["users"]
eventCol = db["events"]
idCol = db["id"]
connectCol = db["userConnect"]
profileCol = db["profile"]


def newID():
    try:
        id = idCol.find()
        idList = list(id)
        oid = json.loads(json_util.dumps(idList))
        returnID = oid[0]["id"] + 1
        return returnID
    except:
        new = {'id': 1}
        idCol.insert_one(new)
        id = idCol.find()
        idList = list(id)
        oid = json.loads(json_util.dumps(idList))
        returnID = oid[0]["id"] + 1
    return returnID


def addEvent(content):
    DP = content["DP"]
    money = int(content["money"])
    email1 = content["email1"]
    email2 = content["email2"]
    user1 = list(profileCol.find({"email": f"{email1}"}))
    user2 = list(profileCol.find({"email": f"{email2}"}))
    users1money = int(user1[0]["money"])
    users2money = int(user2[0]["money"])
    user1name = user1[0]["name"]
    user2name = user2[0]["name"]
    user1firstname = user1[0]["firstname"]
    user2firstname = user2[0]["firstname"]
    event = {
        "DP": DP,
        "money": money,
        "name1": user1name,
        "firstname1": user1firstname,
        "email1": email1,
        "name2": user2name,
        "firstname2": user2firstname,
        "email2": email2,
        "id": newID(),
        "commets": ""
    }
    profileCol.update_one({"email": f"{email1}"}, {'$set': {'money': users1money + money}})
    profileCol.update_one({"email": f"{email2}"}, {'$set': {'money': users2money - money}})
    eventCol.insert_one(event)
    idCol.update_one({}, {'$set': {'id': newID()}})
    return True


def deleteEvent(content):
    delevent = content['id']
    email1 = content["email1"]
    email2 = content["email2"]
    money = int(content["money"])
    user1 = profileCol.find({"email": f"{email1}"})
    users1money = int(list(user1)[0]["money"])
    user2 = profileCol.find({"email": f"{email2}"})
    users2money = int(list(user2)[0]["money"])
    profileCol.update_one({"email": f"{email1}"}, {'$set': {'money': users1money - money}})
    profileCol.update_one({"email": f"{email2}"}, {'$set': {'money': users2money + money}})
    eventCol.delete_one({'id': delevent})
    return True


def editItem(content):
    newmoney = int(content["money"])
    oldmoney = int(content["oldmoney"])
    email1 = content["email1"]
    email2 = content["email2"]
    id= content["id"]
    try:
        comments = content["comments"]
        editsumm(email1=email1, email2=email2, oldmoney=oldmoney, newmoney=newmoney)
        eventCol.update_one({"id": id}, {'$set': {'money': newmoney, "comments": comments}})
        return True
    except:
        editsumm(email1=email1, email2=email2, oldmoney=oldmoney, newmoney=newmoney)
        eventCol.update_one({"id": id}, {'$set': {'money': newmoney}})
        return True