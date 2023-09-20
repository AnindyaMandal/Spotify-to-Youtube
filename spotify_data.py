import os, requests, spotify_oauth, json





# Authenticate user and get access token in env
spotify_oauth.auth()


base_uri = "https://api.spotify.com/v1"
profile_uri = 'https://api.spotify.com/v1/me'

def get_all_playlists():
    access_token = os.environ['SPOTIFY_ACCESS_TOKEN']
    response = requests.get(profile_uri + "/playlists", headers={
        'Authorization': 'Bearer ' + access_token
    })

    # print(response.content.decode("utf-8"))

    data = response.json()
    print("Length of data: num of playlists i think  " + str(len(data["items"])))
    print(data["items"][0]["name"])





get_all_playlists()



