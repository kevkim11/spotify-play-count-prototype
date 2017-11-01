import base64
import requests # API call
import json # store json object in a .json file.
import logging

import os

# google api
from google_sheets import update_google_sheets

# Spotify Credentials
limit = 50
BASE_URL = 'https://api.spotify.com/v1/me/'
FETCH_URL = BASE_URL + 'player/recently-played?limit=' + str(limit)

path = os.path.dirname(os.path.abspath(__file__))
path += "/secret"
logger = logging.getLogger()

def diff(arr1, arr2):
    """
    Compares two arrays and returns an array that's a diff of the two input arrays
    :param arr1:
    :param arr2:
    :return:
    """
    return list(set(arr2)-set(arr1))

def diff_json_obj(arr1, arr2):
    """
    Compares a list of two array's of json track items and returns the diff of the two.
    :param arr1:
    :param arr2:
    :return:
    """
    list_of_timestamps_1 = [item["played_at"] for item in arr1]
    list_of_timestamps_2 = [item["played_at"] for item in arr2]

    dif = list(set(list_of_timestamps_1)-set(list_of_timestamps_2))

    # 4) Get the data based on the dif to add to the table.
    dif_items = []
    for timestamp in dif:
        for item in fetched_items:
            if item["played_at"] == timestamp:
                dif_items.append(item)

    return dif_items

if __name__ == "__main__":

    # 1) Fetch new data
    print "READ spotify json files"
    tokens_file = path + "/tokens.json"
    with open(tokens_file, 'r') as fp:
        tokens = json.load(fp)
        access_token = str(tokens["access_token"])
        refresh_token = str(tokens["refresh_token"])

    spotify_client_secret_file = path + "/spotify_client_secret.json"
    with open(spotify_client_secret_file, 'r') as fp:
        client = json.load(fp)
        client_id = str(client["client_id"])
        client_secret = str(client["client_secret"])

    # Refresh token
    auth_header = base64.b64encode(str(client_id + ':' + client_secret).encode())
    OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'
    headers = {'Authorization': 'Basic %s' % auth_header.decode()}
    payload = {'refresh_token': refresh_token,
               'grant_type': 'refresh_token'}
    print "POST refresh token"
    response = requests.post(OAUTH_TOKEN_URL, data=payload, headers=headers)
    token_info = response.json()
    tokens["access_token"] = token_info["access_token"]

    header = {
        'Authorization': 'Bearer ' + tokens["access_token"]
    }

    print "GET Spotify Recently Played API"
    r = requests.get(FETCH_URL, headers=header)
    content = r.json()
    fetched_items = content["items"]
    list_of_timestamps_2 = [item["played_at"] for item in fetched_items]

    # 2.1) Load saved data
    print "READ previous last played json"
    previous_last_played_file = path + "/previous_last_played.json"
    with open(previous_last_played_file, 'r') as fp:
        data = json.load(fp)

    saved_items = data["items"]
    list_of_timestamps_1 = [item["played_at"] for item in saved_items]

    # 3) Compare the datas based on their time stamps
    dif = diff(list_of_timestamps_1, list_of_timestamps_2)

    # 4) Get the data based on the dif to add to the table.
    dif_items = [item for timestamp in dif for item in fetched_items if item["played_at"] == timestamp]
    print "Number of items to update: " + str(len(dif_items))

    # Google Spread sheet
    if len(dif_items) > 0:
        update_google_sheets(dif_items)

        print "WRITE new last played"
        # Save the fetched data last, after the table has been updated
        with open(previous_last_played_file, 'w') as fp:
            json.dump(content, fp)
    print "WRITE new tokens"
    # Save the refreshed access token
    with open(tokens_file, 'w') as fp:
        json.dump(tokens, fp)