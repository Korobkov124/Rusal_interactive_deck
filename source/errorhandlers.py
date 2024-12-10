from users import app, make_response, jsonify, auth

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'response': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'response': 'Bad request'}), 400)

@auth.error_handler
def unauthorized():
    return make_response(jsonify({"response": "Unathorized access"}), 403)

@app.errorhandler(500)
def internal_error(error):
    return make_response(jsonify({"response": "Internal error"}), 500)
