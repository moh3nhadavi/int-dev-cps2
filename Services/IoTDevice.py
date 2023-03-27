import requests


def get_temperature(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None


def presence_detect(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None
