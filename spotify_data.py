import os, requests, spotify_oauth, SongData, youtube_search, webbrowser



# Authenticate user and get access token in env
spotify_oauth.auth()


song_data_arr = []
base_uri = "https://api.spotify.com/v1"
profile_uri = 'https://api.spotify.com/v1/me'

def get_all_playlists():
    access_token = os.environ['SPOTIFY_ACCESS_TOKEN']
    response = requests.get(profile_uri + "/playlists", headers={
        'Authorization': 'Bearer ' + access_token
    })

    # print(response.content.decode("utf-8"))

    data = response.json()
    num_of_plist = len(data["items"])
    print("Length of data:  " + str(num_of_plist))
    # print(data["items"][0]["name"])

    count = 0
    for plist in data["items"]:
        print(str(count) + ". Name: " + plist["name"] + "\tTrack endpoint: " + plist["tracks"]["href"])
        count += 1

    correct_input = False
    user_select = -1
    while(not correct_input):
        
        try:
            user_select = int(input("Which playlist number would you like more information on? "))
            if user_select < 0 or user_select >= num_of_plist:
                raise ValueError
            
            break

        except ValueError:
            print("Please enter an integer between 0 and " + str(len(data["items"]) - 1))

    
    print("Selected playlist: " + data["items"][user_select]["name"] + "\tID: " + data["items"][user_select]["id"])

    print("Getting track info for playlist ID: " + data["items"][user_select]["id"] + "\t Name: " + data["items"][user_select]["name"])

    selected_plist_id = data["items"][user_select]["id"]

    response = requests.get(base_uri + "/playlists/" + selected_plist_id + "/tracks?limit=50", headers={
        'Authorization': 'Bearer ' + access_token
    })

    track_data = response.json()
    # print(str(track_data) + "\n")
    print(response.status_code)
    print(track_data)
    for track in track_data["items"]:
        print("Track name:\t" + track["track"]["name"])

        print("Artists:\t" + str(track["track"]["artists"][0]["name"]))
        print("Album:\t" + str(track["track"]["album"]["name"]))
        print("Uri:\t" + track["track"]["uri"])


# https://developer.spotify.com/documentation/web-api/reference/get-users-saved-tracks
def get_liked_songs(offset=0):
    access_token = os.environ['SPOTIFY_ACCESS_TOKEN']
    response = requests.get(profile_uri + "/tracks?offset=" + str(offset) + "&limit=50", headers={
        'Authorization': 'Bearer ' + access_token
    })
    
    liked_songs = response.json()
    print("Liked songs length: " + str(len(liked_songs["items"])))
    if len(liked_songs["items"]) == 0: return 0
    for track in liked_songs["items"]:
        # print("Track name:\t" + track["track"]["name"])

        # print("Artists:\t" + str(track["track"]["artists"][0]["name"]))
        # print("Album:\t" + str(track["track"]["album"]["name"]))
        # print("Uri:\t" + track["track"]["uri"])

       
        SongData.data_arr.append(SongData.SongData(str(track["track"]["name"]), track["track"]["artists"][0]["name"], str(track["track"]["album"]["name"])))
    get_liked_songs(offset+50)





get_liked_songs()

print("\n\n\n\t\t PRINTING SONG DATA ARRAY\n\n\n")




youtube_search.get_song_from_YT()

# for song in SongData.data_arr:
#     print("Name: " + str(song.name) + "\tArtists: " + str(song.artist_arr))
#     print("Album: " + str(song.album_name))
#     webbrowser.open(song.url)
    
# get_all_playlists()



