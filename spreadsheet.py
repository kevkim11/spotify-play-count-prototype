import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import os
import json

# scope = ['https://spreadsheets.google.com/feeds']
# creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/kevkim/GitHub/spotify-play-count/secret/google_secret_client.json', scopes=scope)
# client = gspread.authorize(credentials=creds)
#
# sheet = client.open('Spotify Play Count').sheet1
#
# pp = pprint.PrettyPrinter()

path = os.path.dirname(os.path.abspath(__file__))
path += "/secret"

with open('/Users/kevkim/GitHub/spotify-play-count/secret/token.json', 'r') as fp:
    tokens = json.load(fp)

print path
