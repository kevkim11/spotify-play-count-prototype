import os
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# paths
path = os.path.dirname(os.path.abspath(__file__))
path += "/secret"
google_secret_client_file = path + "/google_secret_client.json"

scope = ['https://spreadsheets.google.com/feeds']

def update_google_sheets(dif_items):
    # Google Spread Sheet Credentials
    creds = ServiceAccountCredentials.from_json_keyfile_name(google_secret_client_file, scopes=scope)
    gs_client = gspread.authorize(credentials=creds)
    sheet = gs_client.open('Spotify Play Count').sheet1
    print "ADD/UPDATE google sheets"
    # row = [id, track_name, track_id, artist_name, artist_id, play_count, album_name, album_id, last_played, date_added]
    for item in dif_items:
        all_tracks = sheet.get_all_records()
        result_dict = {}
        for track in all_tracks:
            result_dict[track['track_id']] = track

        track_id = item["track"]["id"] # will use track_id since it's unique
        index = sheet.row_count
        # if session expires, re-login
        if creds.access_token_expired:
            gs_client.login()
        if track_id in result_dict: # if it already exists, update the play count and last played
            already_played_track = result_dict[track_id]
            print "Updating track " + already_played_track["track_name"]
            row_id = already_played_track["id"] + 1
            already_played_track["play_count"] += 1
            sheet.update_cell(row_id, 6, already_played_track["play_count"])
            # Also update last_played
            last_played = item["played_at"]
            sheet.update_cell(row_id, 9, last_played)
        else:
            # insert a new row
            print str(index) + ") it doesn't exist so need to create "+ item["track"]["name"]
            row = [index,
                   item["track"]["name"],
                   item["track"]["id"],
                   item["track"]["artists"][0]["name"],
                   item["track"]["artists"][0]["id"],
                   1, # play count is always 1
                   item["track"]["album"]["name"],
                   item["track"]["album"]["id"],
                   item["played_at"],
                   item["played_at"]
                   ]
            sheet.append_row(row)