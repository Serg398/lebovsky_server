import json
from pymongo import MongoClient
from bson import json_util
from money import editsumm


cluster = MongoClient("mongodb://62.3.58.53", 27017)
db = cluster["lebovsky"]
usersCol = db["users"]
eventCol = db["events"]
idCol = db["id"]
connectCol = db["userConnect"]


def getEmail(useremail):
    email = list(usersCol.find({"Email": f"{useremail}"}))
    if email != []:
        return True


def newID():
    id = idCol.find()
    idList = list(id)
    oid = json.loads(json_util.dumps(idList))
    returnID = oid[0]["id"] + 1
    return returnID


def getAll(profile):
    email = profile
    users = usersCol.find()
    dataProfile = list(usersCol.find({"Email": f"{email}"}))
    usersList = list(users)
    events = eventCol.find().sort("id", -1)
    eventsList = list(events)
    id = idCol.find()
    idList = list(id)
    res = ({"users": usersList, "events": eventsList, "id": idList, "account": dataProfile})
    return json.loads(json_util.dumps(res))


def addEvent(content):
    DP = content["DP"]
    money = int(content["money"])
    Email1 = content["Email1"]
    Email2 = content["Email2"]
    user1 = list(usersCol.find({"Email": f"{Email1}"}))
    user2 = list(usersCol.find({"Email": f"{Email2}"}))
    print(user1, user2)
    users1money = int(user1[0]["money"])
    users2money = int(user2[0]["money"])
    user1name = user1[0]["name"]
    user2name = user2[0]["name"]
    oid = newID()
    event = {
        "DP": DP,
        "money": money,
        "name1": user1name,
        "Email1": Email1,
        "Email2": Email2,
        "name2": user2name,
        "id": oid,
        "commets": ""
    }
    usersCol.update_one({"Email": f"{Email1}"}, {'$set': {'money': users1money + money}})
    usersCol.update_one({"Email": f"{Email2}"}, {'$set': {'money': users2money - money}})
    eventCol.insert_one(event)
    idCol.update_one({}, {'$set': {'id': oid}})
    return True


def deleteEvent(content):
    delevent = content['id']
    Email1 = content["Email1"]
    Email2 = content["Email2"]
    money = int(content["money"])
    user1 = usersCol.find({"Email": f"{Email1}"})
    users1money = int(list(user1)[0]["money"])
    user2 = usersCol.find({"Email": f"{Email2}"})
    users2money = int(list(user2)[0]["money"])
    usersCol.update_one({"Email": f"{Email1}"}, {'$set': {'money': users1money - money}})
    usersCol.update_one({"Email": f"{Email2}"}, {'$set': {'money': users2money + money}})
    eventCol.delete_one({'id': delevent})
    return True


def editItem(content):
    newmoney = int(content["money"])
    oldmoney = int(content["oldmoney"])
    Email1 = content["Email1"]
    Email2 = content["Email2"]
    id= content["id"]
    try:
        comments = content["comments"]
        editsumm(Email1=Email1, Email2=Email2, oldmoney=oldmoney, newmoney=newmoney)
        eventCol.update_one({"id": id}, {'$set': {'money': newmoney, "comments": comments}})
        return True
    except:
        editsumm(Email1=Email1, Email2=Email2, oldmoney=oldmoney, newmoney=newmoney)
        eventCol.update_one({"id": id}, {'$set': {'money': newmoney}})
        return True


def addUser(content):
    content["money"] = 0
    usersCol.insert_one(content)
    return True

def auth2(content):
    email = content["Email"]
    passw = content["pass"]
    usersCol.find({"Email": f"{email}"})
    resp = list(usersCol.find({"Email": f"{email}"}))
    if resp != []:
        resppass = resp[0]["pass"]
        if resppass == passw:
            return True
        else:
            return False
    else:
        return False





