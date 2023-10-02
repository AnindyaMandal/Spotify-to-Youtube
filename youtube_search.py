import re, urllib.request, urllib.parse
import webbrowser
import SongData

# TODO: SongData.data_arr ->  name, artists, album
#       Use that info to query Youtube and get the first search result
# Imp Links:
# https://stackoverflow.com/questions/15959534/visibility-of-global-variables-in-imported-modules
# https://stackoverflow.com/questions/71981616/how-to-search-videos-on-youtube-and-get-link-with-python


def get_song_from_YT():
    for song in SongData.data_arr:
        print("\n\tYouTube Query for: " + song.name + "\t" + str(song.artists))
        artists = str(song.artists)
        yt_query = urllib.parse.urlencode({'search_query' : song.name , ' by ' : artists})
        print("\tQuery: " + yt_query)
        print("\n\thttps://www.youtube.com/results?" + str(yt_query))

        song.query = str("https://www.youtube.com/results?" + yt_query)
        res = urllib.request.urlopen("https://www.youtube.com/results?" + yt_query)
    
        video_ids = re.findall(r"watch\?v=(\S{11})", res.read().decode())

        print("https://www.youtube.com/watch?v=" + video_ids[0])
        song.url = str("https://www.youtube.com/watch?v=" + video_ids[0])

        # webbrowser.open(song.url)



