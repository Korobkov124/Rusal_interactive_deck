from flask import Flask, request, jsonify, abort, make_response



users = [
    {'id': 0,
     'name': 'admin',
     'tg': '@admin',
     'number': '+7(999)999-99-99',
     'email': 'admin@admin.ru',
     'active': True,
     'role': 'admin'},
    {'id': 1,
     'name': 'test',
     'tg': '@test',
     'number': '+7(888)888-88-88',
     'email': 'test@test.ru',
     'active': True,
     'role': 'user'}, 
]

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'response': 'Not found'}), 404)

@app.route('/users', methods=['POST'])
def create_user():
    print(request.json, request.method)
    users.append({'id': request.json['id'],
                  'name': request.json['name'],
                  'tg': request.json['tg'],
                  'number': request.json['number'],
                  'email': request.json['email'],
                  'active': True,
                  'role': 'user'})
    return jsonify({'response': 'ok'})

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    x = list(filter(lambda x: x['id'] == int(id), users))
    if not x:
        abort(404)
    return jsonify({'id': x[0]['id'], 'name': x[0]['name'], 'tg': x[0]['tg'], 'number': x[0]['number'], 'email': x[0]['email'], 'active': x[0]['active'], 'role': x[0]['role']})

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    x = list(filter(lambda x: x['id'] == int(id), users))
    x[0]['name'] = request.json['name'] if 'name' in request.json else x[0]['name']
    x[0]['tg'] = request.json['tg'] if 'tg' in request.json else x[0]['tg']
    x[0]['number'] = request.json['number'] if 'number' in request.json else x[0]['number']
    x[0]['email'] = request.json['email'] if 'email' in request.json else x[0]['email']
    x[0]['active'] = request.json['active'] if 'active' in request.json else x[0]['active']
    print(x[0])
    return jsonify({'response': 'ok'})
    
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    x = list(filter(lambda x: x['id'] == int(id), users))
    if not x:
        abort(404)
    x[0]['active'] = False
    return jsonify({'response': 'ok'})
if __name__ == '__main__':
    app.run(debug=True)

# curl -i -H "Content-Type: application/json" http://localhost:5000/users/ -d '{"id":2,"name":"test1"}'
# curl -i http://localhost:5000/users/0