from flask import Flask
import datetime

app = Flask(__name__)

timedelta = [{
    "id": 0,
    "id_owner": 0,
    "coworking": 1,
    "time_start": datetime.datetime.now(),
    "time_end": datetime.datetime.now(),
    "active": True
},
{
    "id": 1,
    "id_owner": 0,
    "coworking": 2,
    "time_start": datetime.datetime.now(),
    "time_end": datetime.datetime.now(),
    "active": True
}]

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