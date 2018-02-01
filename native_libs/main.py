from spotify_play_count import *
from google_sheets import update_google_sheets
import json

if __name__ == "__main__":

    access_token = get_spotify_access_token()

    content = get_spotify_recently_played(access_token)
    fetched_items = content["items"]

    # 1) Load saved data
    print "READ previous last played json"
    data_str = previous_last_played_aws.get()['Body'].read()
    saved_items = json.loads(data_str)["items"]
    # with open(previous_last_played_file, 'r') as fp:
    #     saved_items = json.load(fp)["items"]

    # 2) Get the data based on the dif to add to the table.
    dif_items = diff_json_obj(fetched_items, saved_items)

    print "Number of items to update: " + str(len(dif_items))

    # Google Spread sheet - only update when there are dif_items
    if len(dif_items) > 0:
        update_google_sheets(dif_items)
        print "WRITE new last played"
        # Save the fetched data last, after the table has been updated
        previous_last_played_aws.put(Body=json.dumps(content))
        # with open(previous_last_played_file, 'w') as fp:
        #     json.dump(content, fp)
    else:
        print "Nothing was updated"