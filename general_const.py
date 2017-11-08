import os

# Paths
path = os.path.dirname(os.path.abspath(__file__))
path += "/secret"
refresh_token_file = path + "/refresh_token.json"
spotify_client_secret_file = path + "/spotify_client_secret.json"
previous_last_played_file = path + "/previous_last_played.json"
google_secret_client_file = path + "/google_secret_client.json"

