from flask import Flask, jsonify, request, Response, session
from flask_cors import CORS
from mongo import getAll
from events import addEvent, deleteEvent, editItem
from profile import newProfile
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash


cluster = MongoClient("mongodb://127.0.0.1", 27017)
db = cluster["lebovsky"]
usersCol = db["users"]
eventCol = db["events"]
idCol = db["id"]
connectCol = db["userConnect"]
profileCol = db["profile"]


app = Flask(__name__)
app.secret_key = 'the random string'
app.config['SECRET_KEY'] = 'super secret key'
cors = CORS(app, resources={r"/api": {"origins": "*", "allow_headers": "*", "expose_headers": "*"}})
CORS(app, supports_credentials=True)



@app.route('/api/index', methods=['GET'])
def getlist():
    profile = session.get('email')
    print(profile)
    if 'email' in session:
        if getAll(profile=profile) == False:
            return jsonify({"text": "render(auth)", "status": 204})
        else:
            return getAll(profile=profile)



@app.route('/api/login', methods=['POST'])
def login():
    content = request.json
    email = content["Email"]
    print("Запрос на вход: ", email)
    passw = content["pass"]
    profileMongo = list(profileCol.find({"email": f"{email}"}))
    if profileMongo == []:
        return jsonify({"text": "Пользователь не найден", "status": 204})
    else:
        passProfileMongo = profileMongo[0]["passwd"]
        if check_password_hash(passProfileMongo, passw) == True:
            session['email'] = email
            print("Вход: ", email)
            return jsonify({"text": "Добро пожаловать", "status": 200})
        else:
            return jsonify({"text": "Неверный логин или пароль", "status": 204})


@app.route('/api/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        session.pop('email', None)
        resp = jsonify({"text": "logout", "status": 204})
        resp.set_cookie('email', expires=0)
        return resp


@app.route('/api/additem', methods=['POST'])
def additem():
    content = request.json
    if addEvent(content=content) == True:
        return jsonify()


@app.route('/api/delitem', methods=['POST'])
def delitem():
    content = request.json
    if deleteEvent(content=content) == True:
        return jsonify()


@app.route('/api/edititem', methods=['POST'])
def edititem():
    content = request.json
    if editItem(content=content) == True:
        return jsonify()


@app.route('/api/register', methods=['POST'])
def register():
    content = request.json
    if newProfile(content=content) == True:
        print("Новый пользователь: ", content)
        return Response("RegisterOK", status=200)
