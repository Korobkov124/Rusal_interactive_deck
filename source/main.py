from users import app, make_response, jsonify, update_user, get_user, delete_user, create_user, auth
from errorhandlers import not_found, bad_request, unauthorized
from booking import get_booking, get_bookings, create_booking, delete_booking, update_booking
from data import *


if __name__ == '__main__':
    app.run(debug=True)

# curl -i -H "Content-Type: application/json" http://localhost:5000/users/ -d @json.txt
# curl -i -H "Content-Type: application/json" -X PUT http://localhost:5000/users/2 -d @json1.txt
# curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/users/2
# curl -i http://localhost:5000/users/2


