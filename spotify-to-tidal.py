# takes a spotify public playlist URL and returns the tidalLister command
# python3 ./spotify-to-tidal.py "thisSpotifyURL"

import sys
import re
import requests
from bs4 import BeautifulSoup

url = sys.argv[1]
# url = "https://open.spotify.com/playlist/6gNwLjuyLIK6rl4LV0jkch"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")

playlist = soup.title.get_text().replace(" | Spotify", "").replace(" - playlist", "")
# then remove ' - playlist' & ' | Spotify'
# print(playlist)

tracksDict = []

tracks = soup.select('[data-testid="track-row"]')
# print(tracks)
for track in tracks:
    try:
        links = track.select("a[href]")
        songRaw = links[0].get_text()
        songRaw = songRaw.replace(",", " ").replace("/", " ").replace("\\", " ")
        songRaw = songRaw.replace("'", "").replace('"', "")
        song = re.sub("'\"\s\’\”", "", songRaw.replace("  ", " "))
        artistRaw = links[1].get_text()
        artistRaw = artistRaw.replace(",", " ").replace("/", " ").replace("\\", " ")
        artistRaw = artistRaw.replace("'", "").replace('"', "")
        artist = re.sub("'\"\s\’\”", "", artistRaw.replace("  ", " "))
        print(song, artist)
        tracksDict.append(song + " " + artist)
    except:
        print("Had an error. Moving on")
        print(links)

tracksForCLI = ", ".join(tracksDict)

command = [
    "./tidallister.py",
    f"-K='{tracksForCLI}'",
    "-S=5",
    "-SD=5",
    f"-P='{playlist}'",
]
commandString = " ".join(command)
print("\n*** Now copy this code and run it to make the Tidal playlist ***\n")
print("python3 " + commandString)
