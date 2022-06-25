# Include standard modules
import argparse
import json

# Tidal API - https://github.com/tamland/python-tidal && https://tidalapi.netlify.app/api.html#
import tidalapi

playlistPrefix = "TidalLister: "
useDefaultPlaylistName = True
newPlaylistDescription = "Generated by TidalLister. \n"

# Initiate the parser
parser = argparse.ArgumentParser()
parser.add_argument(
    "-A", "--artists", help="comma separated list of arists to search for"
)
parser.add_argument(
    "-T",
    "--tracks",
    help="same as -K, comma separated list of tracks to search for",
)
parser.add_argument(
    "-G", "--genres", help="comma separated list of genres to search for"
)
parser.add_argument(
    "-L", "--albums", help="comma separated list of albums to search for"
)
parser.add_argument(
    "-K", "--keywords", help="comma separated list, top tracks of each search term"
)
parser.add_argument(
    "-S",
    "--similars",
    help="the number of similar artists to get extra tracks from (only works if -A is declared) (default is 3)",
)
parser.add_argument(
    "-SD",
    "--similarsdeep",
    help="use true/false or 1/0, this goes deeper and gets similars of similars (only works if -A & -S are declared) (** BE CAREFUL: this makes your playlist grow exponentially!**)",
)
parser.add_argument(
    "-AD",
    "--allowdupes",
    help="use true/false or 1/0, this allows duplicates if true, default is to skip duplicates",
)
parser.add_argument(
    "-P",
    "--playlist",
    help="the name of the playlist to create, optional, will be prefixed with '"
    + playlistPrefix
    + "'",
)
parser.add_argument(
    "-Q",
    "--qty",
    help="the number of songs from each search to add (default is 10 for each artist/genre/keyword)",
)

# Read arguments from the command line
args = parser.parse_args()

# Store arg values
print("Creating a Tidal Playlist using the following input...")
if (artists := args.artists) is not None:
    artists = str(args.artists).strip()
    print(" > artists:", artists)
if (albums := args.albums) is not None:
    albums = str(args.albums).strip()
    print(" > albums:", albums)
if (genres := args.genres) is not None:
    genres = str(args.genres).strip()
    print(" > genres:", genres)
if (similars := args.similars) is not None:
    similars = str(args.similars).strip()
    print(" > similars:", similars)
if (similarsdeep := args.similarsdeep) is not None:
    similarsdeep = str(args.similarsdeep).strip()
    print(" > similarsdeep:", similarsdeep)
if (allowdupes := args.allowdupes) is not None:
    allowdupes = str(args.allowdupes).strip()
    print(" > allowdupes:", allowdupes)
if (playlist := args.playlist) is not None:
    playlist = str(args.playlist).strip()
    print(" > playlist:", playlist)
if (qty := args.qty) is not None:
    qty = str(args.qty).strip()
    print(" > qty:", qty)
else:
    qty = 10
# track search just uses keyword, so show provided values
# but then merge them if they both exist
if (tracks := args.tracks) is not None:
    tracks = str(args.tracks).strip()
    print(" > tracks:", tracks)
if (keywords := args.keywords) is not None:
    keywords = str(args.keywords).strip()
    print(" > keywords:", keywords)


# Build lists to use later
artistsList = []
albumsList = []
genresList = []
keywordsList = []
tracksToAdd = []
artistsIDs = []


# set up defaults
if not int(qty):
    qty = 10
else:
    qty = int(qty)

if allowdupes:
    allowdupes = bool(json.loads(str(allowdupes).lower()))

letsGoDeep = False
if not similars:
    getSimilars = False
    similars = 0
else:
    getSimilars = True
    if similarsdeep:
        letsGoDeep = True
    if not int(similars):
        similars = 3
    else:
        similars = int(similars)

if not playlist:
    useDefaultPlaylistName = True
    playlist = playlistPrefix
else:
    useDefaultPlaylistName = False
    playlist = playlistPrefix + playlist + " - "

if artists:
    artistsList = artists.split(",")
    playlist += " " + " ".join(artists.split(","))
    newPlaylistDescription += "--artists '" + artists + "' "
    if similars:
        playlist += " (& Similar Artists)"
        newPlaylistDescription += "--similars='" + str(similars) + "' "
        if similarsdeep:
            playlist += " [DEEP]"
            newPlaylistDescription += "--similarsdeep='" + str(similarsdeep) + "' "


if albums:
    albumsList = albums.split(",")
    playlist += " " + " ".join(albums.split(","))
    newPlaylistDescription += "--albums '" + albums + "' "

if genres:
    genresList = genres.split(",")
    playlist += " " + " ".join(genres.split(","))
    newPlaylistDescription += "--genres '" + genres + "' "

if tracks:
    # track search just uses keyword search
    playlist += " " + " ".join(tracks.split(","))
    # newPlaylistDescription += "--tracks '" + tracks + "' "
    if not keywords:
        keywords = tracks
    else:
        keywords += ", " + tracks

if keywords:
    keywordsList.append(keywords.split(","))
    playlist += " " + " ".join(keywords.split(","))
    newPlaylistDescription += "--keywords '" + keywords + "' "


# custom method to remove bracket text
def remove_bracket_text(test_str):
    ret = ""
    skip1c = 0
    skip2c = 0
    for i in test_str:
        if i == "[":
            skip1c += 1
        elif i == "(":
            skip2c += 1
        elif i == "]" and skip1c > 0:
            skip1c -= 1
        elif i == ")" and skip2c > 0:
            skip2c -= 1
        elif skip1c == 0 and skip2c == 0:
            ret += i
    return ret


# return track name as a unique string ID
# Given: "Heroes (Live) [Album Version]"
# Returns: "heroes"
# So that duplicates (even live versions) can be identified
def make_string_id(test_str):
    ret = str(test_str)
    if not allowdupes:
        ret = remove_bracket_text(ret)
    ret = ret.lower().strip().replace(" ", "")
    ret = "".join(char for char in ret if char.isalnum())
    return ret


# Connect to Tidal
session = tidalapi.Session()
# Will run until you visit the printed url and link your account
session.login_oauth_simple()
userID = session.user.id


## TODO:
def get_all_tracks_from_all_albums(artistID):
    # return list of track ids
    pass


def get_artist_radio(artistID):
    # return list of track ids
    pass


def get_track_radio(trackID):
    # return list of track ids
    pass


# https://tidalapi.netlify.app/_modules/tidalapi.html#Session.get_artist_similar
def get_artist_similar(artistID):
    # return list of track ids
    pass


def get_similars(artistID, artistName, goDeep=False):
    print("Getting", similars, "artists similar to", artistName, "...")
    # if there are no similar artists, the response if 404 error
    try:
        similarArtists = session.get_artist_similar(artistID)
        similarsFound = 0
        for i, sim in enumerate(similarArtists):
            if sim.id not in artistsIDs:
                if similarsFound == int(similars):
                    break
                else:
                    similarsFound += 1
                    artistsIDs.append(sim.id)
                    print(
                        artistName,
                        "* SIMILAR ARTIST #",
                        similarsFound,
                        ":",
                        sim.name,
                        sim.id,
                    )
            else:
                print(
                    artistName,
                    "* SIMILAR ARTIST",
                    sim.name,
                    sim.id,
                    "but they're already in the list",
                )
            if goDeep:
                print("\nGoing Deep...")
                get_similars(sim.id, artistName + " > " + sim.name, False)
    except Exception as e:
        print(e, "\n")
    print(" ")


# END get_similars


# Search for the artists
if artists:
    for a in artistsList:
        print(" - - - \n")
        print("* Searching for ARTIST:", a)
        search = session.search("artist", a, limit=1)
        if search.artists:
            for result in search.artists:
                artistID = result.id
                # add all artist IDs to list, then loop through to get tracks
                if artistID not in artistsIDs:
                    artistsIDs.append(artistID)
                    print("** Found ARTIST:", result.name, artistID)
                else:
                    print(
                        "** Found ARTIST:",
                        result.name,
                        artistID,
                        "and they're already in the list",
                    )
                if getSimilars:
                    get_similars(artistID, result.name, letsGoDeep)
                # END if getSimilars:
        # END if search.artists:


# Loop through artistsIDs and add tracks
if artistsIDs:
    print(" - - - \n")
    for artistID in artistsIDs:
        print("Getting Tracks for artistID:", artistID, "\n")
        topTracks = session.get_artist_top_tracks(artistID)
        # collect track titles so we can avoid duplicates
        trackTitles = []
        for i, track in enumerate(topTracks):
            trackID = str(track.id)
            trackStringID = make_string_id(track.name) + make_string_id(
                track.artist.name
            )
            trackInfoForPrint = (
                trackID
                + " - "
                + track.name
                + " by "
                + track.artist.name
                + " * "
                + trackStringID
            )
            if int(qty) == len(trackTitles):
                break
            else:
                if trackStringID not in trackTitles:
                    tracksToAdd.append(trackID)
                    trackTitles.append(trackStringID)
                    print("  +Added!", trackInfoForPrint)
                else:
                    print("  -Duplicate:", trackInfoForPrint)
        print("\n")


# Search for the albums
if albums:
    for a in albumsList:
        print(" - - - \n")
        print("* Searching for ALBUMS: ", a)
        search = session.search("album", a, limit=1)
        if search.albums:
            for result in search.albums:
                albumID = result.id
                print("** Found ALBUM: ", result.name, albumID, "\n")
                albumTracks = session.get_album_tracks(albumID)
                trackTitles = []
                for i, track in enumerate(albumTracks):
                    trackID = str(track.id)
                    trackStringID = make_string_id(track.name) + make_string_id(
                        track.artist.name
                    )
                    trackInfoForPrint = (
                        trackID
                        + " - "
                        + track.name
                        + " by "
                        + track.artist.name
                        + " * "
                        + trackStringID
                    )
                    if trackStringID not in trackTitles:
                        tracksToAdd.append(trackID)
                        trackTitles.append(trackStringID)
                        print("  +Added!", trackInfoForPrint)
                    else:
                        print("  -Duplicate:", trackInfoForPrint)
        print("\n")


# Search for the genres (by finding the first playlist named for the genre)
if genres:
    for a in genresList:
        print(" - - - \n")
        print("* Searching for GENRES: ", a)
        search = session.search("playlist", a, limit=1)
        if search.playlists:
            for result in search.playlists:
                playlistID = result.id
                print("** Found GENRE Playlist: ", result.name, playlistID, "\n")
                genreTracks = session.get_playlist_tracks(playlistID)
                trackTitles = []
                for i, track in enumerate(genreTracks):
                    trackID = str(track.id)
                    trackStringID = make_string_id(track.name) + make_string_id(
                        track.artist.name
                    )
                    trackInfoForPrint = (
                        trackID
                        + " - "
                        + track.name
                        + " by "
                        + track.artist.name
                        + " * "
                        + trackStringID
                    )
                    if int(qty) == len(trackTitles):
                        break
                    else:
                        if trackStringID not in trackTitles:
                            tracksToAdd.append(trackID)
                            trackTitles.append(trackStringID)
                            print("  +Added!", trackInfoForPrint)
                        else:
                            print("  -Duplicate:", trackInfoForPrint)
        print("\n")


# Search for the keywords (by finding the top tracks for each keyword)
if keywords:
    for a in keywordsList:
        print(" - - - \n")
        print("* Searching for KEYWORDS: ", a)
        # we'll pad the qty a bit in case of duplicates so that we get more than enough results and can then limit it to the qty
        search = session.search("track", a, limit=(int(qty) + 10))
        if search.tracks:
            print("** Found KEYWORD results: ", a, "\n")
            trackTitles = []
            for i, track in enumerate(search.tracks):
                trackID = str(track.id)
                trackStringID = make_string_id(track.name) + make_string_id(
                    track.artist.name
                )
                trackInfoForPrint = (
                    trackID
                    + " - "
                    + track.name
                    + " by "
                    + track.artist.name
                    + " * "
                    + trackStringID
                )
                if int(qty) == len(trackTitles):
                    break
                else:
                    if trackStringID not in trackTitles:
                        tracksToAdd.append(trackID)
                        trackTitles.append(trackStringID)
                        print("  +Added!", trackInfoForPrint)
                    else:
                        print("  -Duplicate:", trackInfoForPrint)
        print("\n")


if tracksToAdd:
    print("\nMaking a new playlist with", len(tracksToAdd), "tracks...\n")
    # Create new playlist
    newPlaylistName = " ".join(playlist.split())
    newPlaylistName = newPlaylistName.strip()
    newPlaylistDescription += "--qty '" + str(qty) + "' "
    newPlaylist = session.request(
        "POST",
        "users/%s/playlists" % userID,
        data={"title": newPlaylistName, "description": newPlaylistDescription},
    )
    newPlaylistID = newPlaylist.json()["uuid"]
    # print(newPlaylistID)

    # Add Tracks to playlist
    # to_index = 0
    etag = session.request("GET", "playlists/%s" % newPlaylistID).headers["ETag"]
    headers = {"if-none-match": etag}
    data = {"trackIds": ",".join(tracksToAdd)}
    result = session.request(
        "POST", "playlists/%s/tracks" % newPlaylistID, data=data, headers=headers
    )
    newPlaylistURL = "https://tidal.com/browse/playlist/" + newPlaylistID
    print(
        "\n",
        "Done! Your New Playlist '",
        newPlaylistName,
        "'\n",
        "is now available at",
        newPlaylistURL,
        "\n",
    )
