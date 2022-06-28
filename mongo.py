import json
from pymongo import MongoClient
from bson import json_util


cluster = MongoClient("mongodb://62.3.58.53", 27017)
db = cluster["lebovsky"]
usersCol = db["users"]
eventCol = db["events"]
idCol = db["id"]
connectCol = db["userConnect"]
profileCol = db["profile"]


def getAll(profile):
    account = profile
    users = []
    for itemUser in profileCol.find():
        users.append({
            'name': itemUser['name'],
            'firstname': itemUser['firstname'],
            'money': itemUser['money'],
            'email': itemUser['email']
        })
    dataAccount = setAccount(account=account)
    events = list(eventCol.find().sort("id", -1))
    res = {
        'users': users,
        "events": events,
        'account': dataAccount
    }
    return json.loads(json_util.dumps(res))


def setAccount(account):
    dataAccount = list(profileCol.find({"email": f"{account}"}))
    print(dataAccount)
    dataAccount[0].pop('passwd')
    oAccount = {
                'data': dataAccount,
                'settings': {
                    'ok': 1,
                    'no': 2
                },
                'history': []
                }
    return oAccount















