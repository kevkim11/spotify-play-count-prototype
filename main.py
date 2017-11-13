from spotify_play_count import *
from google_sheets import update_google_sheets

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

    # Google Spread sheet - only update when there are dif_items
    if len(dif_items) > 0:
        update_google_sheets(dif_items)
        print "WRITE new last played"
        # Save the fetched data last, after the table has been updated
        with open(previous_last_played_file, 'w') as fp:
            json.dump(content, fp)
    else:
        print "Nothing was updated"