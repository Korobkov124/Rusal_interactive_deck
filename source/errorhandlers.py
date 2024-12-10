from users import app, make_response, jsonify

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

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'response': 'Not found'}), 404)