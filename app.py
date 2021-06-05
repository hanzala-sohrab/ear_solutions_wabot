from flask import Flask, request, jsonify
from datetime import datetime
import requests
from flask_pymongo import PyMongo
from requests.structures import CaseInsensitiveDict
import foo

app = Flask(__name__)

app.config["MONGO_URI"] = foo.MONGO_URI
mongo = PyMongo(app)
db_operations = mongo.db.users

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
    if len(name) > 1:
        lead['firstName'] = name[0]
        lead['lastName'] = " ".join(name[1:])
        record.set_field_value('First_Name', lead['firstName'])
    else:
        lead['lastName'] = " ".join(name)
    
    lead['mobile'] = user['_id']
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
    return resp

@app.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        foobar = request.json
        phone = foobar['waId']
        message = foobar['text']
        print(message)
        user = db_operations.find_one({'_id': int(phone)})
        if user is None:
            new_user = {'_id': int(phone), 'returnMessage': "Foo"}
            db_operations.insert_one(new_user)
            user = db_operations.find_one({'_id': int(phone)})
        try:
            value = user['returnMessage']
        except:
            value = "Foo"

        if message in ["Hi", "hi", "Hello", "hello", "Hey", "hey"]:
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
                return save(row=r)
        elif "Person" in value:
            if message == '1':
                person = "For Myself"
            else:
                person = "For Someone Else"
            update = {"$set": {"returnMessage": "Existing", "person": person}}
            db_operations.update_one(user, update)
        elif "Existing" in value:
            if message == '1' or message == 'y' or message == 'Y':
                message = "Yes"
            elif message == '2' or message == 'n' or message == 'N':
                message = "No"
            update = {"$set": {"returnMessage": "Connecting", "existing": message}}
            db_operations.update_one(user, update)
            return save(row=r)
    return 'NoCommand'

if(__name__) == '__main__':
    app.run()
