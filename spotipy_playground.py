import json
import base64
import requests # API call

# Spotify Credentials
limit = 50
BASE_URL = 'https://api.spotify.com/v1/me/'
FETCH_URL = BASE_URL + 'player/recently-played?limit=' + str(limit)

if __name__=="__main__":

    with open('./secret/refresh_token.json', 'r') as fp:
        tokens = json.load(fp)
        refresh_token = str(tokens["refresh_token"])

    with open('./secret/spotify_client_secret.json', 'r') as fp:
        client = json.load(fp)
        client_id = str(client["client_id"])
        client_secret = str(client["client_secret"])

    auth_header = base64.b64encode(str(client_id + ':' + client_secret).encode())
    OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'
    headers = {'Authorization': 'Basic %s' % auth_header.decode()}
    payload = {'refresh_token': refresh_token,
               'grant_type': 'refresh_token'}
    response = requests.post(OAUTH_TOKEN_URL,
                             data=payload,
                             headers=headers)
    token_info = response.json()
    with open('./secret/tokens.json', 'w') as fp:
        json.dump(tokens, fp)

    header = {
        'Authorization': 'Bearer ' + token_info["access_token"]
    }
    print "GET Spotify Recently Played API"
    r = requests.get(FETCH_URL, headers=header)
    content = r.json()

    with open('./secret/previous_last_played.json', 'w') as fp:
        json.dump(content, fp)