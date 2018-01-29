import base64
import requests
import json

from general_const import *
import sys

# Spotify URL Credentials
limit = 50 # Max limit
BASE_URL = 'https://api.spotify.com/v1/me/'
FETCH_URL = BASE_URL + 'player/recently-played?limit=' + str(limit)


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

    dif_tracks = [item for timestamp in dif for item in arr1 if item["played_at"] == timestamp]

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
    # with open(spotify_client_secret_file, 'r') as fp:
    #     client = json.load(fp)
    #     client_id = str(client["client_id"])
    #     client_secret = str(client["client_secret"])
    #     refresh_token = str(client["refresh_token"])
    client_str = spotify_client_secret_json
    client = json.loads(client_str)
    client_id = str(client["client_id"])
    client_secret = str(client["client_secret"])
    refresh_token = str(client["refresh_token"])

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
        return None
    token_info = response.json()
    return token_info["access_token"]

def get_spotify_recently_played(access_token):
    """
    Need to write/store the returned json object to previous_last_played at the end of the script.
    :param access_token:
    :return: json object
    """
    header = {'Authorization': 'Bearer ' + access_token}
    print "GET Spotify Recently Played API"
    r = requests.get(FETCH_URL, headers=header)
    content = r.json()
    # fetched_items = content["items"]
    return content

if __name__ == "__main__":
    """
    Initialize previous_last_played.json
    
    previous_last_played.json is empty when first downloaded. Need to populate with the latest
    Current User's Recently Played Tracks (play history object)
    
    Run this script when this project is first downloaded and prior to running main.py
    """
    with open(spotify_client_secret_file, 'r') as fp:
        client = json.load(fp)
        client_id = str(client["client_id"])
        client_secret = str(client["client_secret"])
        refresh_token = str(client["refresh_token"])

    auth_header = base64.b64encode(str(client_id + ':' + client_secret).encode())
    OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'
    headers = {'Authorization': 'Basic %s' % auth_header.decode()}
    payload = {'refresh_token': refresh_token,
               'grant_type': 'refresh_token'}

    response = requests.post(OAUTH_TOKEN_URL, data=payload, headers=headers)
    if response.status_code != 200:
        print "error!"
        print "response.status_code = " + str(response.status_code)

    token_info = response.json()

    header = {
        'Authorization': 'Bearer ' + token_info["access_token"]
    }
    print "GET Spotify Recently Played API"
    r = requests.get(FETCH_URL, headers=header)
    content = r.json()

    with open(previous_last_played_file, 'w') as fp:
        json.dump(content, fp)
        print "Successfully Finished!"
