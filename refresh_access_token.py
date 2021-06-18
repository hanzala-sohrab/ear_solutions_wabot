import foo, requests, json
from requests.structures import CaseInsensitiveDict

def refresh_token():
    url = f"{foo.refreshURL}?refresh_token={foo.refresh_token}&client_id={foo.client_id}&client_secret={foo.client_secret}&grant_type=refresh_token"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    resp = requests.post(url, headers=headers)
    print(resp.json())
    return json.loads(resp.text)


if __name__ == "__main__":
    refresh_token()