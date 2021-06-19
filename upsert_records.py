import requests, json, foo, refresh_access_token
from refresh_access_token import refresh_token

def upsert(lead):

    url = 'https://www.zohoapis.in/crm/v2/Leads/upsert'

    headers = {
        'Authorization': f"Zoho-oauthtoken {refresh_token()['access_token']}"
    }

    request_body = dict()
    record_list = list()

    record_list.append(lead)

    request_body['data'] = record_list

    duplicate_check_fields = ['Mobile']

    request_body['duplicate_check_fields'] = duplicate_check_fields

    trigger = [
        'approval',
        'workflow',
        'blueprint'
    ]

    request_body['trigger'] = trigger

    response = requests.post(url=url, headers=headers, data=json.dumps(request_body).encode('utf-8'))

    if response is not None:
        return response.json()

if __name__ == "__main__":
    lead = {
        "Last_Name": "Foobar",
        "Mobile": "919999999999"
    }
    upsert(lead=lead)