from flask import request, jsonify, abort, make_response, url_for
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
from data import users, app, generate_password_hash, check_password_hash, connect_db

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
    if any(x['username'] == request.json['username'] for x in users):
        abort(400)
    data_new_user = {'id': users[-1]["id"] + 1,
                  'username': request.json['username'],
                  'name': request.json['name'],
                  'tg': request.json['tg'],
                  'number': request.json['number'],
                  'email': request.json['email'],
                  'active': True,
                  'role': 'admin',
                  'password': generate_password_hash(request.json['password'])}
    users.append(data_new_user)
    with connect_db() as connection:
        cursor = connection.cursor()
        placeholders = ', '.join(['?'] * len(users[-1].keys()))
        sql = f"INSERT INTO users VALUES ({placeholders})"
        cursor.execute(sql, list(users[-1].values()))
        connection.commit()
    return jsonify({'response': 'ok'})


@app.route('/users', methods=['GET'])
# @auth.login_required
def get_users():
    # if list(filter(lambda x: x['username'] == auth.current_user(), users))[0]['role'] == 'user':
        # abort(403)
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
    return jsonify({'response': {'id': x[0]['id'], 
                                 'name': x[0]['name'], 
                                 'username': x[0]['username'], 
                                 'tg': x[0]['tg'], 
                                 'number': x[0]['number'],
                                 'email': x[0]['email'],
                                 'active': x[0]['active'], 
                                 'role': x[0]['role']}})

@app.route('/users/<int:id>', methods=['PUT'])
# @auth.login_required
def update_user(id):
    # if list(filter(lambda x: x['username'] == auth.current_user(), users))[0]['role'] == 'user' and list(filter(lambda x: x['username'] == auth.current_user(), users))[0]['id'] != id:
        # abort(403)
    x = list(filter(lambda x: x['id'] == int(id), users))
    for key in request.json.keys():
        if key == 'password':
            x[0][key] = generate_password_hash(request.json[key])
            continue
        x[0][key] = request.json[key]
    with connect_db() as connection:
        cursor = connection.cursor()
        sql = f"UPDATE users SET {', '.join([f'{key} = ?' for key in x[0].keys()])} WHERE id = ?"
        cursor.execute(sql, list(x[0].values())[:-1] + [generate_password_hash(x[0]['password'])] + [id])
        connection.commit() 

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
    with connect_db() as connection:
        cursor = connection.cursor()
        sql = f"UPDATE users SET active = ? WHERE id = ?"
        cursor.execute(sql, [x[0]['active'], x[0]['id']])
        connection.commit()
    return jsonify({'response': 'ok'})