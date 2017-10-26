import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/kevkim/GitHub/spotify-play-count/secret/google_secret_client.json', scopes=scope)
client = gspread.authorize(credentials=creds)

sheet = client.open('Spotify Play Count').sheet1

pp = pprint.PrettyPrinter()

# for i in range(3):
#     result = sheet.get_all_records()
#     index = sheet.row_count
#     print index
#     row = [index, "Cooler than Cool", 'adagwerqw2', 'Jin Kim', 'zialk849q', '1', 'album_name','album_id','last_played', 'date_added']
#     sheet.append_row(row)

# result = sheet.get_all_records()
# count = sheet.row_count
# row1 = sheet.row_values(2)

# pp.pprint(result)
