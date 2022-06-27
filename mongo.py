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


def getAll(profile):
    account = profile
    users = usersCol.find()
    dataAccount = getAccount(account=account)
    usersList = list(users)
    events = eventCol.find().sort("id", -1)
    eventsList = list(events)
    id = idCol.find()
    idList = list(id)
    res = {
        "users": usersList,
        "events": eventsList,
        "id": idList,
        'account': dataAccount
    }
    return json.loads(json_util.dumps(res))



def setAccount():
    return


def getAccount(account):
    dataAccount = list(usersCol.find({"Email": f"{account}"}))
    dataAccount[0].pop('pass')
    oAccount = {
                'data': dataAccount,
                'settings': {'ok': 1, 'no': 2},
                'history': []
                }
    return oAccount


def newID():
    id = idCol.find()
    idList = list(id)
    oid = json.loads(json_util.dumps(idList))
    returnID = oid[0]["id"] + 1
    return returnID





def addEvent(content):
    DP = content["DP"]
    money = int(content["money"])
    Email1 = content["Email1"]
    Email2 = content["Email2"]
    user1 = list(usersCol.find({"Email": f"{Email1}"}))
    user2 = list(usersCol.find({"Email": f"{Email2}"}))
    users1money = int(user1[0]["money"])
    users2money = int(user2[0]["money"])
    user1name = user1[0]["name"]
    user2name = user2[0]["name"]
    user1firstname = user1[0]["firstname"]
    user2firstname = user2[0]["firstname"]
    oid = newID()
    event = {
        "DP": DP,
        "money": money,
        "name1": user1name,
        "firstname1": user1firstname,
        "Email1": Email1,
        "name2": user2name,
        "firstname2": user2firstname,
        "Email2": Email2,
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


def registrationM(content):
    contentPass = content['pass']
    contentPassHash = generate_password_hash(contentPass)
    content['pass'] = contentPassHash
    content["money"] = 0
    usersCol.insert_one(content)
    return True


def loginM(content):
    email = content["Email"]
    passw = content["pass"]
    usersCol.find({"Email": f"{email}"})
    respM = list(usersCol.find({"Email": f"{email}"}))
    if respM != []:
        resppass = respM[0]["pass"]
        if check_password_hash(resppass, passw) == True:
            return True
        else:
            return False
    else:
        return False






