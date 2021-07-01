from flask import Flask, request, jsonify
from datetime import datetime
import requests
from flask_pymongo import PyMongo
from requests.structures import CaseInsensitiveDict
import foo
import json
from upsert_records import upsert

application = Flask(__name__)

application.config["MONGO_URI"] = foo.MONGO_URI
mongo = PyMongo(application)
db_operations = mongo.db.users

APIUrl = foo.APIUrl
token = foo.token

def get_message(phone):
    url = f"{APIUrl}api/v1/getMessages/{phone}"
    headers = {"Authorization": token}
    answer = requests.get(url, headers=headers)
    return answer.json()

@application.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        foobar = request.json
        phone = foobar['waId']
        message = foobar['text']
        user = db_operations.find_one({'_id': int(phone)})
        if user is None:
            new_user = {
                '_id': int(phone), 
                'returnMessage': "Foo",
                "name": "Foo Bar",
                "concern": "Book an Appointment",
                "person": "For Myself",
                "existing": "No"
            }
            db_operations.insert_one(new_user)
            user = db_operations.find_one({'_id': int(phone)})
        try:
            value = user['returnMessage']
        except:
            value = "Foo"

        if message in ["Hi", "hi", "Hello", "hello", "Hey", "hey"]:
            lead = {
                "Last_Name": "User",
                "Mobile": phone,
                "Lead_Source": "Website",
                "Secondary_Source": "Whatsapp"
            }
            resp = upsert(lead)
            db_operations.delete_one({'_id': int(phone)})
            new_user = {
                '_id': int(phone),
                "ID": resp['data'][0]['details']['id'],
                'returnMessage': "Foo",
                "name": "User",
                "concern": "Book an Appointment",
                "person": "For Myself",
                "existing": "No"
            }
            db_operations.insert_one(new_user)
            user = db_operations.find_one({'_id': int(phone)})
            update = {"$set": {"returnMessage": "Name"}}
            db_operations.update_one(user, update)
        elif "Name" in value:
            name = message.split()
            if len(name) > 1:
                lead = {
                    "First_Name": name[0],
                    "Last_Name": " ".join(name[1:]),
                    "Phone": phone,
                    "Mobile": phone
                }
            else:
                lead = {
                    "Last_Name": message,
                    "Phone": phone,
                    "Mobile": phone
                }
            resp = upsert(lead)
            update = {"$set": {"returnMessage": "Concern", "name": message}}
            db_operations.update_one(user, update)
        elif "Concern" in value:
            if message in ["Book an Appointment", "Hearing Aid Trial"]:
                returnMessage = "Person"
            else:
                returnMessage = "Thank you"
            lead = {
                "Concern": message,
                "Mobile": phone
            }
            resp = upsert(lead)
            update = {"$set": {"returnMessage": returnMessage, "concern": message}}
            db_operations.update_one(user, update)
        elif "Person" in value:
            if message == '1':
                person = "For Myself"
            else:
                person = "For Someone Else"
            lead = {
                "For_whom": person,
                "Mobile": phone
            }
            resp = upsert(lead)
            update = {"$set": {"returnMessage": "Existing", "person": person}}
            db_operations.update_one(user, update)
        elif "Existing" in value:
            if message in ['1', 'y', 'Y']:
                message = "Yes"
            else:
                message = "No"
            lead = {
                "Existing_Aid_User": message,
                "Mobile": phone
            }
            resp = upsert(lead)
            update = {"$set": {"returnMessage": "Connecting", "existing": message}}
            db_operations.update_one(user, update)
    return 'NoCommand'

if(__name__) == '__main__':
    application.run(port=8000)
