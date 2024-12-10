from users import app, jsonify, abort, request, auth
from data import booking, users
import datetime


@app.route('/booking', methods=['GET'])
@auth.login_required
def get_bookings():
    return_booking = list(filter(lambda x: x['active'] == True, booking))
    return jsonify({"response": return_booking})

@app.route('/booking/free', methods=['GET'])
def get_free_bookings():
    bookings = list(filter(lambda x: x['active'] == False and (datetime.datetime.strptime(x['time_start'], "%Y-%m-%d %H:%M") < datetime.datetime.now() or datetime.datetime.strptime(x['time_end'], "%Y-%m-%d %H:%M") > datetime.datetime.now())), booking)
    return jsonify({"response": bookings})

@app.route('/booking/<int:id>', methods=['GET'])
def get_booking(id):
    x = list(filter(lambda x: x['id'] == int(id) and x['active'] == True, booking))
    if not x:
        abort(404)
    return jsonify({'response': {"id": x[0]['id'], "id_owner": x[0]['id_owner'], "coworking": x[0]['coworking'], "time_start": x[0]['time_start'], "time_end": x[0]['time_end'], "active": x[0]['active']}})

@app.route('/booking/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_booking(id):
    if list(filter(lambda x: x['username'] == auth.current_user(), users))[0]['role'] == 'user' and list(filter(lambda x: x['username'] == auth.current_user(), users))[0]['id'] != id:
        abort(403)
    x = list(filter(lambda x: x['id'] == int(id), booking))
    if not x:
        abort(404)
    x[0]['active'] = False
    return jsonify({'response': 'ok'})

@app.route('/booking', methods=['POST'])
@auth.login_required
def create_booking():
    if any(x['id'] == request.json['id'] for x in booking):
        abort(400)
    booking.append({'id': request.json['id'],
                      'id_owner': list(filter(lambda x: x['username'] == auth.current_user(), users))[0]['id'],
                      'coworking': request.json['coworking'], 
                      'time_start': request.json['time_start'],
                      'time_end': request.json['time_end'],
                      'active': True})
    return jsonify({'response': 'ok'})

@app.route('/booking/<int:id>', methods=['PUT'])
@auth.login_required
def update_booking(id):
    if list(filter(lambda x: x['username'] == auth.current_user(), users))[0]['role'] == 'user' and list(filter(lambda x: x['username'] == auth.current_user(), users))[0]['id'] != id:
        abort(403)
    x = list(filter(lambda x: x['id'] == int(id), booking))
    x[0]['coworking'] = request.json['coworking'] if 'coworking' in request.json else x[0]['coworking']
    x[0]['time_start'] = request.json['time_start'] if 'time_start' in request.json else x[0]['time_start']
    x[0]['time_end'] = request.json['time_end'] if 'time_end' in request.json else x[0]['time_end']
    return jsonify({'response': 'ok'})
