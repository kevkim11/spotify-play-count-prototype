import json
import base64
import requests # API call

from datetime import datetime

# Spotify Credentials
limit = 50
BASE_URL = 'https://api.spotify.com/v1/me/'
FETCH_URL = BASE_URL + 'player/recently-played?limit=' + str(limit)

if __name__=="__main__":



    right_now = datetime.today()
    print right_now