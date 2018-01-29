from spotify_play_count import *
from google_sheets import update_google_sheets
import boto3
import json
from general_const import *

if __name__ == "__main__":
    # s3 = boto3.resource('s3')
    #
    #
    # google_secret_client_aws = s3.Object('spotifyplaycount', 'secret/google_secret_client.json')
    # spotify_client_secret_aws = s3.Object('spotifyplaycount', 'secret/spotify_client_secret.json')
    # previous_last_played_aws = s3.Object('spotifyplaycount', 'secret/previous_last_played.json')


    with open(google_secret_client_file, 'r') as fp:
        data = json.load(fp)
    with open(spotify_client_secret_file, 'r') as fp:
        spotify_data = json.load(fp)
    with open(previous_last_played_file, 'r') as fp:
        previous_data = json.load(fp)
    # google_secret_client_aws.put(Body=json.dumps(data))
    # data = google_secret_client_aws.get()['Body'].read()
    # spotify_client_secret_aws.put(Body=json.dumps(spotify_data))
    # data = spotify_client_secret_aws.get()['Body'].read()

    previous_last_played_aws.put(Body=json.dumps(previous_data))
    data = previous_last_played_aws.get()['Body'].read()

    print data
    pretty_data = json.loads(data)
    # for k, v in pretty_data.iteritems():
    #     print k + ':' + v

    for k in pretty_data:
        print k
    # print pretty_data




# if __name__ == "__main__":
#
#     access_token = get_spotify_access_token()
#
#     content = get_spotify_recently_played(access_token)
#     fetched_items = content["items"]
#
#     # 2.1) Load saved data
#     print "READ previous last played json"
#     with open(previous_last_played_file, 'r') as fp:
#         data = json.load(fp)
#     saved_items = data["items"]
#
#     # 3) Get the data based on the dif to add to the table.
#     dif_items = diff_json_obj(fetched_items, saved_items)
#
#     print "Number of items to update: " + str(len(dif_items))
#
#     # Google Spread sheet - only update when there are dif_items
#     if len(dif_items) > 0:
#         update_google_sheets(dif_items)
#         print "WRITE new last played"
#         # Save the fetched data last, after the table has been updated
#         with open(previous_last_played_file, 'w') as fp:
#             json.dump(content, fp)
#     else:
#         print "Nothing was updated"