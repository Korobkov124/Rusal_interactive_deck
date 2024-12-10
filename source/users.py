from flask import request, jsonify, abort, make_response, url_for
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
from data import users, app, generate_password_hash, check_password_hash

def make_public_id(id):
    new_id = {}
    for field in id:
        if field == 'id':
            new_id['URL'] = url_for('get_user', id=id[field], _external=True)
        else:
            new_id[field] = id[field]
    return new_id

@auth.verify_password
def verify_password(username, password):
    for user in users:
        if user['username'] == username and check_password_hash(user["password"], password):
            return username
    
@auth.get_password
def get_password(username):
    if username in users:
        print(users.get(username))
        return users.get(username)['password']
    return None



@app.route('/users', methods=['POST'])
def create_user():
    users.append({'id': request.json['id'],
                  'username': request.json['username'],
                  'name': request.json['name'],
                  'tg': request.json['tg'],
                  'number': request.json['number'],
                  'email': request.json['email'],
                  'active': True,
                  'role': 'user',
                  'password': generate_password_hash(request.json['password'])})
    return jsonify({'response': 'ok'})


@app.route('/users', methods=['GET'])
@auth.login_required
def get_users():
    if list(filter(lambda x: x['username'] == auth.current_user(), users))[0]['role'] == 'user':
        abort(403)
    x = list(filter(lambda x: x['active'] == True, users))
    return jsonify({'response': list(map(make_public_id, x))})

@app.route('/users/<int:id>', methods=['GET'])
@auth.login_required
def get_user(id):
    if list(filter(lambda x: x['username'] == auth.current_user(), users))[0]['role'] == 'user' and list(filter(lambda x: x['username'] == auth.current_user(), users))[0]['id'] != id:
        abort(403)
    x = list(filter(lambda x: x['id'] == int(id), users))
    if not x:
        abort(404)
    return jsonify({'response': {'id': x[0]['id'], 'name': x[0]['name'], 'username': x[0]['username'], 'tg': x[0]['tg'], 'number': x[0]['number'], 'email': x[0]['email'], 'active': x[0]['active'], 'role': x[0]['role']}})

@app.route('/users/<int:id>', methods=['PUT'])
@auth.login_required
def update_user(id):
    if list(filter(lambda x: x['username'] == auth.current_user(), users))[0]['role'] == 'user' and list(filter(lambda x: x['username'] == auth.current_user(), users))[0]['id'] != id:
        abort(403)
    x = list(filter(lambda x: x['id'] == int(id), users))
    x[0]['name'] = request.json['name'] if 'name' in request.json else x[0]['name']
    x[0]['username'] = request.json['username'] if 'username' in request.json else x[0]['username']
    x[0]['tg'] = request.json['tg'] if 'tg' in request.json else x[0]['tg']
    x[0]['number'] = request.json['number'] if 'number' in request.json else x[0]['number']
    x[0]['email'] = request.json['email'] if 'email' in request.json else x[0]['email']
    x[0]['active'] = request.json['active'] if 'active' in request.json else x[0]['active']
    x[0]['password'] = request.json['password'] if 'password' in request.json else x[0]['password']
    print(x[0])
    return jsonify({'response': 'ok'})
    
@app.route('/users/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_user(id):
    if list(filter(lambda x: x['username'] == auth.current_user(), users))[0]['role'] == 'user' and list(filter(lambda x: x['username'] == auth.current_user(), users))[0]['id'] != id:
        abort(403)
    x = list(filter(lambda x: x['id'] == int(id), users))
    if not x:
        abort(404)
    x[0]['active'] = False
    return jsonify({'response': 'ok'})