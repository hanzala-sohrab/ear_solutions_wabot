from flask import Flask, request, jsonify
from datetime import datetime
import requests
from flask_pymongo import PyMongo
from requests.structures import CaseInsensitiveDict
import foo
from zcrmsdk import ZCRMRestClient, ZCRMRecord, ZCRMModule
import json

application = Flask(__name__)

application.config["MONGO_URI"] = foo.MONGO_URI
mongo = PyMongo(application)
db_operations = mongo.db.users

configuration_dictionary = {
    'apiBaseUrl': foo.apiBaseUrl,
    'apiVersion': 'v2',
    'currentUserEmail': foo.currentUserEmail,
    'sandbox': 'False',
    'applicationLogFilePath': './log/',
    'client_id': foo.client_id,
    'client_secret': foo.client_secret,
    'redirect_uri': 'https://www.abc.com',
    'accounts_url': 'https://accounts.zoho.in',
    'token_persistence_path': '.',
    'access_type': 'online'
}

ZCRMRestClient.get_instance().initialize(configuration_dictionary)

APIUrl = foo.APIUrl
token = foo.token

def get_message(phone):
    url = f"{APIUrl}api/v1/getMessages/{phone}"
    headers = {"Authorization": token}
    answer = requests.get(url, headers=headers)
    return answer.json()

def save(user):
    lead = {}
    record = ZCRMRecord.get_instance('Leads')
    name = user['name'].split()
    if len(name) > 1:
        lead['firstName'] = name[0]
        lead['lastName'] = " ".join(name[1:])
        record.set_field_value('First_Name', lead['firstName'])
    else:
        lead['lastName'] = " ".join(name)
    record.set_field_value('Last_Name', lead['lastName'])

    lead['mobile'] = str(user['_id'])
    record.set_field_value('Mobile', lead['mobile'])

    concern = user['concern']
    if concern in ['Book an Appointment', 'Hearing Aid Trial']:
        lead['person'] = user['person']
        lead['personAlreadyAidUser'] = user['existing']
        record.set_field_value('For_whom', lead['person'])
        record.set_field_value('Existing_Hearing_Aid_User?', lead['personAlreadyAidUser'])
    
    record.set_field_value('Lead_Source', "Website")
    record.set_field_value('Secondary_Source', "Whatsapp")

    lead = json.dumps(lead, indent = 4)
    print(lead)
    resp = record.create()
    print(resp.status_code, " ", resp.code)
    response = {
        "status_code": resp.status_code,
        "code": resp.code
    }
    return json.loads(json.dumps(response))

@application.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        foobar = request.json
        phone = foobar['waId']
        message = foobar['text']
        # print(message)
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
            db_operations.delete_one({'_id': int(phone)})
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
            update = {"$set": {"returnMessage": "Name"}}
            db_operations.update_one(user, update)
        elif "Name" in value:
            update = {"$set": {"returnMessage": "Concern", "name": message}}
            db_operations.update_one(user, update)
        elif "Concern" in value:
            if message in ["Book an Appointment", "Hearing Aid Trial"]:
                returnMessage = "Person"
            else:
                returnMessage = "Thank you"
            update = {"$set": {"returnMessage": returnMessage, "concern": message}}
            db_operations.update_one(user, update)
            if message == "Customer Support":
                return save(user=user)
        elif "Person" in value:
            if message == '1':
                person = "For Myself"
                update = {"$set": {"returnMessage": "Existing", "person": person}}
                db_operations.update_one(user, update)
            elif message in ['2', '3']:
                person = "For Someone Else"
                update = {"$set": {"returnMessage": "Existing", "person": person}}
                db_operations.update_one(user, update)
        elif "Existing" in value:
            if message in ['1', 'y', 'Y']:
                message = "Yes"
            else:
                message = "No"
            update = {"$set": {"returnMessage": "Connecting", "existing": message}}
            db_operations.update_one(user, update)
            return save(user=user)
    return 'NoCommand'

if(__name__) == '__main__':
    application.run(port=8000)
