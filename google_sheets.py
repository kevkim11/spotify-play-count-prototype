import gspread
from oauth2client.service_account import ServiceAccountCredentials
from general_const import *

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
        if creds.access_token_expired: # if session expires, re-login
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
            artists_name_list = [artist["name"] for artist in item["track"]["artists"]]
            artists_name_str = ', '.join(artists_name_list)
            row = [index,
                   item["track"]["name"],
                   item["track"]["id"],
                   artists_name_str,
                   item["track"]["artists"][0]["id"],
                   1, # first listen
                   item["track"]["album"]["name"],
                   item["track"]["album"]["id"],
                   item["played_at"],
                   item["played_at"]
                   ]
            sheet.append_row(row)

def total_play_count():
    # Google Spread Sheet Credentials
    creds = ServiceAccountCredentials.from_json_keyfile_name(google_secret_client_file, scopes=scope)
    gs_client = gspread.authorize(credentials=creds)
    sheet = gs_client.open('Spotify Play Count').sheet1
    play_count_list = sheet.col_values(6)
    play_count_list = play_count_list[1:]
    play_count_list = map(int, play_count_list) # py3 -> list(map(int, play_count_list))
    print play_count_list
    return sum(play_count_list)
