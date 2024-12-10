from users import app, jsonify, abort, request, auth
from data import booking, users, connect_db
import datetime
from xlsxwriter import Workbook


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
    with connect_db() as connection:
        cursor = connection.cursor()
        sql = f"UPDATE booking SET active = ? WHERE id = ?"
        cursor.execute(sql, [x[0]['active'], x[0]['id']])
        connection.commit()
    return jsonify({'response': 'ok'})

@app.route('/booking', methods=['POST'])
@auth.login_required
def create_booking():
    booking.append({'id': booking[-1]["id"] + 1,
                      'id_owner': list(filter(lambda x: x['username'] == auth.current_user(), users))[0]['id'],
                      'coworking_id': request.json['coworking_id'], 
                      'time_start': request.json['time_start'],
                      'time_end': request.json['time_end'],
                      'active': True,
                      'active_history': True})
    with connect_db() as connection:
        cursor = connection.cursor()
        placeholders = ', '.join(['?'] * len(booking[-1].keys()))
        sql = f"INSERT INTO booking VALUES ({placeholders})"
        cursor.execute(sql, list(booking[-1].values()))
        connection.commit()
    return jsonify({'response': 'ok'})

@app.route('/booking/<int:id>', methods=['PUT'])
@auth.login_required
def update_booking(id):
    if list(filter(lambda x: x['username'] == auth.current_user(), users))[0]['role'] == 'user' and list(filter(lambda x: x['username'] == auth.current_user(), users))[0]['id'] != id:
        abort(403)
    x = list(filter(lambda x: x['id'] == int(id), booking))
    for key in request.json.keys():
        x[0][key] = request.json[key]
    with connect_db() as connection:
        cursor = connection.cursor()
        sql = f"UPDATE booking SET {', '.join([f'{key} = ?' for key in x[0].keys()])} WHERE id = ?"
        print(sql, list(x[0].values()) + [id])
        cursor.execute(sql, list(x[0].values()) + [id])
        connection.commit()
    return jsonify({'response': 'ok'})

@app.route('/booking/stats', methods=['GET'])
def get_stats():
    start = datetime.datetime.now() - datetime.timedelta(days=30)
    end = datetime.datetime.now()
    stats = list(filter(lambda x: datetime.datetime.strptime(x['time_start'], "%Y-%m-%d %H:%M") > start and datetime.datetime.strptime(x['time_end'], "%Y-%m-%d %H:%M") < end, booking))
    booked = {}
    for event in stats:
        if event['coworking_id'] not in booked.keys():
            booked[event['coworking_id']] = [0, datetime.timedelta(0)] #number, sum
        booked[event['coworking_id']][0] += 1
        booked[event['coworking_id']][1] += datetime.datetime.strptime(event['time_end'], "%Y-%m-%d %H:%M") - datetime.datetime.strptime(event['time_start'], "%Y-%m-%d %H:%M")
    workbook = Workbook('stats.xlsx')
    worksheet = workbook.add_worksheet()
    for key in booked.keys():
        worksheet.write(key, 0, key)
        worksheet.write(key, 1, booked[key][0])
        worksheet.write(key, 2, str(booked[key][1]))
    workbook.close()

    return jsonify({"response": "ok"})

@app.route('/recomendation', methods=['POST'])
def get_recomendation():
    number_of_humans = request.json['']