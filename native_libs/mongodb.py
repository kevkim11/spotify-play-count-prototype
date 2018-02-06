# -*- coding: utf-8 -*-
import pymongo
from spotify_play_count import *

def update_mongodb_doc(dif_items):
    # access_token = get_spotify_access_token()
    # content = get_spotify_recently_played(access_token)
    # fetched_items = content["items"]
    # # 1) Load saved data
    # print "READ previous last played json"
    # data_str = previous_last_played_aws.get()['Body'].read()
    # saved_items = json.loads(data_str)["items"]
    #
    # # 2) Get the data based on the dif to add to the table.
    # dif_items = diff_json_obj(fetched_items, saved_items)
    # print "Number of items to update: " + str(len(dif_items))

    # ACTUAL NOW
    # MongoDB Client
    client = pymongo.MongoClient('localhost', 27017)
    db = client.pymongo_test  # It doesn’t actually matter if your specified database has been created yet. By specifying this database name and saving data to it, you create the database automatically.
    played_songs = db.played_songs

    for item in dif_items:
        # .find({}) is inside the for loop due to duplicates
        cursor = played_songs.find({})
        result_dict = {}
        for track in cursor:
            # print i
            result_dict[track['id']] = track
        track_id = item["track"]["id"]  # will use track_id since it's unique
        # if creds.access_token_expired: # if session expires, re-login --> TODO: DO THIS FOR MONGO
        #     gs_client.login()
        if track_id in result_dict: # if it already exists, update the play count and last played
            already_played_track = result_dict[track_id]
            print "Updating track " + already_played_track["name"]
            played_songs.update({"id": track_id}, {"$push": {"timestamps": item["played_at"]}})
            new_play_count = already_played_track["play_count"] + 1
            played_songs.update({"id": track_id}, {"$set": {"play_count": new_play_count}})
        else:
            print " it doesn't exist so need to create " + item["track"]["name"]
            track_obj = item["track"]
            track_obj["timestamps"] = [item["played_at"]]  # list of timestamps
            track_obj["play_count"] = 1
            result = played_songs.insert(track_obj)

def initialize_mongodb():
    access_token = get_spotify_access_token()
    content = get_spotify_recently_played(access_token)
    fetched_items = content["items"]

    # ####### MONGO #######
    #
    client = pymongo.MongoClient('localhost', 27017)
    db = client.pymongo_test # It doesn’t actually matter if your specified database has been created yet. By specifying this database name and saving data to it, you create the database automatically.
    played_songs = db.played_songs

    for i in fetched_items:
        cursor = played_songs.find({})
        result_dict = {}
        for track in cursor:
            result_dict[track['id']] = track
        track_id = i["track"]["id"]
        if track_id in result_dict:  # if it already exists, update the play count and last played
            pass
        else:
            track_obj = i["track"]
            track_obj["timestamps"] = [i["played_at"]] # list of timestamps
            track_obj["play_count"] = 1
            played_songs.insert(track_obj)

if __name__ == "__main__":

    # initialize_mongodb()

    update_mongodb_doc()

    print "finished"


