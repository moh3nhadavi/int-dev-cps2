import requests
import json

def get_temperature(url):
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    return None


def presence_detection(url):
    response = requests.get(url)
    if response.status_code == 200:
        json_data = json.loads(response.text)
        if json_data["connected"] == "1":
            return True
        else:
            return False
    return None
