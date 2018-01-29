import os
import boto3
"""LOCAL"""
# Paths
path = os.path.dirname(os.path.abspath(__file__))
path += "/secret"
# File names
refresh_token_file = path + "/refresh_token.json"
spotify_client_secret_file = path + "/spotify_client_secret.json"
previous_last_played_file = path + "/previous_last_played.json"
google_secret_client_file = path + "/google_secret_client.json"

"""AWS"""
s3 = boto3.resource('s3')
# Read Only
google_secret_client_json = s3.Object('spotifyplaycount', 'secret/google_secret_client.json').get()['Body'].read()
spotify_client_secret_json = s3.Object('spotifyplaycount', 'secret/spotify_client_secret.json').get()['Body'].read()
# Read and Write
previous_last_played_json = s3.Object('spotifyplaycount', 'secret/previous_last_played.json')