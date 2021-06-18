import requests, json, foo, refresh_access_token
from refresh_access_token import refresh_token

def upsert():

    url = 'https://www.zohoapis.in/crm/v2/Leads/upsert'

    headers = {
        'Authorization': f"Zoho-oauthtoken {refresh_token()['access_token']}"
    }

    request_body = dict()
    record_list = list()

    record_object_1 = {
        'Last_Name': 'Changed-Name-1',
        'Email': 'newcrmapi@zoho.com',
        'Company': 'Zoho',
        'Lead_Status': 'Contacted',
    }

    record_list.append(record_object_1)

    record_object_2 = {
        'Last_Name': 'New Lead-3',
        'Email': 'newlead@zoho.com',
        'Lead_Status': 'Attempted to Contact',
        'Phone': '9887766540',
    }

    record_list.append(record_object_2)

    request_body['data'] = record_list

    duplicate_check_fields = ['Email']

    request_body['duplicate_check_fields'] = duplicate_check_fields

    trigger = [
        'approval',
        'workflow',
        'blueprint'
    ]

    request_body['trigger'] = trigger

    response = requests.post(url=url, headers=headers, data=json.dumps(request_body).encode('utf-8'))

    if response is not None:
        print("HTTP Status Code : " + str(response.status_code))

        print(response.json())

if __name__ == "__main__":
    upsert()