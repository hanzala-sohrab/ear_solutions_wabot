import foo, requests, json
from requests.structures import CaseInsensitiveDict

def refresh_token():
    url = f"{foo.refreshURL}?refresh_token={foo.refresh_token}&client_id={foo.client_id}&client_secret={foo.client_secret}&grant_type=refresh_token"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    return requests.post(url, headers=headers).text


if __name__ == "__main__":
    print(refresh_token())