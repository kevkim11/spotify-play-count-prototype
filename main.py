import base64
import requests # API call
import json # store json object in a .json file.

import os
import sys

# google api
from google_sheets import update_google_sheets

# Spotify Credentials
limit = 50
BASE_URL = 'https://api.spotify.com/v1/me/'
FETCH_URL = BASE_URL + 'player/recently-played?limit=' + str(limit)

# Paths
path = os.path.dirname(os.path.abspath(__file__))
path += "/secret"
refresh_token_file = path + "/refresh_token.json"
spotify_client_secret_file = path + "/spotify_client_secret.json"
previous_last_played_file = path + "/previous_last_played.json"

def diff_json_obj(arr1, arr2):
    """
    Compares a list of two array's of json track items and returns the diff of the two.
    :param arr1: array of json objects - most recently played tracks
    :param arr2: array of json objects - previously played tracks
    :return:
    """
    list_of_timestamps_1 = [item["played_at"] for item in arr1]
    list_of_timestamps_2 = [item["played_at"] for item in arr2]

    dif = list(set(list_of_timestamps_1)-set(list_of_timestamps_2))

    dif_tracks = [item for timestamp in dif for item in fetched_items if item["played_at"] == timestamp]

    return dif_tracks

def get_spotify_access_token():
    """
    Using spotify's
    * client_id
    * client_secret
    * refresh_token
    get a new spotify access token
    :return: spotify access token
    """
    # 1) Fetch new data
    print "READ spotify json files"
    with open(refresh_token_file, 'r') as fp:
        token = json.load(fp)
        refresh_token = str(token["refresh_token"])

    with open(spotify_client_secret_file, 'r') as fp:
        client = json.load(fp)
        client_id = str(client["client_id"])
        client_secret = str(client["client_secret"])

    # Refresh token
    OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'
    payload = {'refresh_token': refresh_token,
               'grant_type': 'refresh_token'}

    if sys.version_info[0] >= 3:  # Python 3
        auth_header = base64.b64encode(str(client_id + ':' + client_secret).encode())
        headers = {'Authorization': 'Basic %s' % auth_header.decode()}
    else:  # Python 2
        auth_header = base64.b64encode(client_id + ':' + client_secret)
        headers = {'Authorization': 'Basic %s' % auth_header}

    print "POST refresh token"
    response = requests.post(OAUTH_TOKEN_URL, data=payload, headers=headers)
    if response.status_code != 200:
        print "response.status_code = " + str(response.status_code)
        # return None
    token_info = response.json()
    return token_info["access_token"]

def get_spotify_recently_played(access_token):
    """

    :param access_token:
    :return:
    """
    header = {
        'Authorization': 'Bearer ' + access_token
    }
    print "GET Spotify Recently Played API"
    r = requests.get(FETCH_URL, headers=header)
    content = r.json()
    fetched_items = content["items"]
    return content

if __name__ == "__main__":

    access_token = get_spotify_access_token()

    content = get_spotify_recently_played(access_token)
    fetched_items = content["items"]

    # 2.1) Load saved data
    print "READ previous last played json"
    with open(previous_last_played_file, 'r') as fp:
        data = json.load(fp)
    saved_items = data["items"]

    # 3) Get the data based on the dif to add to the table.
    dif_items = diff_json_obj(fetched_items, saved_items)

    print "Number of items to update: " + str(len(dif_items))

    # Google Spread sheet
    if len(dif_items) > 0:
        update_google_sheets(dif_items)
        print "WRITE new last played"
        # Save the fetched data last, after the table has been updated
        with open(previous_last_played_file, 'w') as fp:
            json.dump(content, fp)