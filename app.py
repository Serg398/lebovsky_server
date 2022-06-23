from flask import Flask, jsonify, request, Response, session,   make_response
from flask_cors import CORS, cross_origin
from mongo import getAll, addEvent, deleteEvent, editItem, addUser, auth2


app = Flask(__name__)
app.secret_key = 'the random string'
app.config['SECRET_KEY'] = 'super secret key'
cors = CORS(app, resources={r"/api": {"origins": "*", "allow_headers": "*", "expose_headers": "*"}})
CORS(app, supports_credentials=True)


@app.route('/api/index', methods=['GET'])
def getlist():
    profile = session.get('email')
    if 'email' in session:
        data = getAll(profile=profile)
        return data
    else:
        return jsonify({"text": "render(auth)", "status": 204})


@app.route('/api/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        content = request.json
        print(content)
        if auth2(content=content) == True:
            session['email'] = content['Email']
            return jsonify({"text": "render(index)", "status": 200})
        else:
            return jsonify({"text": "Такого пользователя не существует", "status": 204})


@app.route('/api/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        session.pop('email', None)
        return jsonify({"text": "render(auth)", "status": 204})


@app.route('/api/additem', methods=['POST'])
def additem():
    content = request.json
    if addEvent(content=content) == True:
        return jsonify()


@app.route('/api/delitem', methods=['POST'])
def delitem():
    content = request.json
    if deleteEvent(content=content) == True:
        print("DEL EVENT: ", content)
        return jsonify()


@app.route('/api/edititem', methods=['POST'])
def edititem():
    content = request.json
    if editItem(content=content) == True:
        print("EDIT EVENT: ", content)
        return jsonify()


@app.route('/api/register', methods=['POST'])
def register():
    content = request.json
    if addUser(content=content) == True:
        print("EDIT EVENT: ", content)
        return Response("RegisterOK", status=200)


