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

    response = requests.get(base_uri + "/playlists/" + selected_plist_id + "/tracks?offset=10&limit=50", headers={
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







    






get_all_playlists()



