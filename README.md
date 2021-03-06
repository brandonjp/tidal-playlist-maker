# tidal-playlist-maker
TidalLister - command line python script that will generate a Tidal playlist from input such as artist, album, genre, keyword, etc.

## example 1: the basics
`python3 ./tidallister.py -A "Harry Nilsson, Amy Grant" -L "Bringing Down the Horse" -G "Jazz" -K "piano cover" -Q=5`

👆 that line would generate a playlist with this 👇: 
 * 5 songs from the artist Harry Nilsson
 * 5 songs from the artist Amy Grant
 * all songs from the album Bringing Down the Horse
 * 5 songs in the Jazz genre
 * 5 songs matching the keyword phrase "piano cover"

You can see the resulting playlist here:  http://tidal.com/browse/playlist/8fbc08ab-6f76-41fb-97df-60f0bff4095f

## example 2: similars & deep
`python3 ./tidallister.py -A "Harry Nilsson, Amy Grant" -L "Bringing Down the Horse" -G "Jazz" -K "piano cover" -Q=5 -S=2 -SD=1`

👆 that line would generate the same playlist as the first example, but the `-S=2 -SD=1` would add this 👇: 
* the `-S=2` would add
  * 5 additional songs from 2 artists similar to Harry Nilsson (in this case, Todd Rundgren & Roxy Music)
  * 5 additional songs from 2 artists similar to Amy Grant
* the `-SD=1` (it's just a true/false option) would add
  * an additional 5 songs from 2 artists similar to the previous similars (in this case, 2 similar to Todd Rundgren & 2 similar to Roxy Music)
  * plus the same for artists that are similar to Amy Grant's similar artists

Confusing? yea. You can view the result here: http://tidal.com/browse/playlist/d59ab08c-7bdc-404c-9351-e07e3c0169f6

**NOTE:** Be aware... the whole `similar artists` thing can get out of hand very quickly. Your playlist will grow exponentially. I don't know what Tidal's caps are on how often you can hit the api or how many tracks you can add to one playlist, but I've hit those limits several times. It's not that bad, it may just crash the python script or worst case make a playlist that's empty.  

Another example:
* `-A=Jewel -Q=5` : if you only search one artist & get 5 tracks, you'll get a 5 song playlist - https://tidal.com/browse/playlist/e31beb4c-91ae-4368-a823-236d0488f29a
* `-A=Jewel -Q=5 -S=2` : if you add similars, that's 3 artists with 5 tracks from each, so 15 tracks - https://tidal.com/browse/playlist/43cb6b61-0eb2-4b4b-9895-4baab53eb843
* `-A=Jewel -Q=5 -S=2 -SD=1` : if you add similarsdeep (it's just a true/false option), you'll get 7 artists, so 35 tracks - https://tidal.com/browse/playlist/2d1ad29a-2329-4843-a816-ac1110ae7c2d

But it can be worth trying to set the quantity low and the similars high, such as:  
`-A=Jewel -Q=1 -S=20 -SD=1` 
which will grab Jewel, then 20 similar artists and then for each of those, 20 similars and then 1 track from each artist
You can see the result here: https://tidal.com/browse/playlist/1b408b0b-c6b8-4699-a7ca-6452ed682c33
(which I thought would only 420 tracks but it's 436 🤷‍♀️)

## example 3: tracks & duplicates

Let's say you want every version of one particular song...

`python3 ./tidallister.py -T="Virtual Insanity" -Q=100`

👆 that line would generate a playlist with this 👇: 
 * tracks matching "Virtual Insanity" from different artists
 * with a maximum of 100 total tracks

You can see the resulting playlist here: https://tidal.com/browse/playlist/f97cb865-e249-4ff0-9136-29b02975aba5

A `-T` or `--tracks` search is actually just the same as a `-K` or `--keywords` search. The `--tracks` option is just a shortcut because I kept forgetting `keywords` would find tracks.

Since the default check for duplicates removes any text in brackets/parens, that means all of the following would be considered the same song. Only the first match found would be added and the rest would be discarded as duplicates:
 * Virtual Insanity by Jamiroquai 
 * Virtual Insanity (Remastered) by Jamiroquai 
 * Virtual Insanity (Bklava Remix) by Jamiroquai
 * Virtual Insanity (Salaam Remi Remix) by Jamiroquai
 * Virtual Insanity (Bklava Remix - Radio Edit) by Jamiroquai
 * Virtual Insanity (Live at the Verona Amphitheatre, Italy, 2002) by Jamiroquai

So what if you wanted to collect ALL of those versions, even if they might be duplicates? Use `-AD=1` or `--allowdupes=1`

`python3 ./tidallister.py -T="Virtual Insanity" -Q=100 -AD=true`

👆 that line would generate a playlist with this 👇: 
 * tracks matching "Virtual Insanity" from different artists
 * with a maximum of 100 total tracks
 * including duplicates (but not exact name dupes)

You can see the resulting playlist here: https://tidal.com/browse/playlist/00e81116-9be3-4712-a223-651e3d32c54e

Allowing Dupes would mean that anything in parenthesis in the track name will be used to consider if the track is a duplicate.  So when `-AD=1` (or true or anything but false), then you'll get live and remastered and remix versions. Some duplicates are still removed. For example, if "Virtual Insanity (Remastered) by Jamiroquai" shows up in the search multiple times because it appears on multiple albums, then it will only be added once. 

The real joy of this is you can quickly grab all (or top) versions of multiple songs with something like: 

`python3 ./tidallister.py -T="new radicals get what you give, santana game of love" -Q=500 -AD=1`

👆 that line would generate a playlist with this 👇: 
 * up to 500 songs matching "New Radicals You Get What You Give"
 * up to 500 songs matching "Santana Game of Love"
 * (in this case there are only a few matches because the search was fairly specific)

You can see the resulting playlist here: https://tidal.com/browse/playlist/ec0b94af-f43e-4147-954f-b0d36783379a

By making the search less specific & removing the artist name, you'll get a much bigger playlist (some songs accurately matching & some less so)...

`python3 ./tidallister.py -T="you get what you give, game of love" -Q=500 -AD=1`

...over 300 tracks with titles that are moderately close matching. You can see the resulting playlist here: https://tidal.com/browse/playlist/38eed1f0-996b-4c7c-b660-75d510f46b7d

## example 4: Spotify playlists

Let's say there's a Spotify playlist you want to listen to, but you'd rather use Tidal...

`python3 ./tidallister.py -SP="https://open.spotify.com/playlist/3cS0NFVjjZlcR7mstctEYT"`

👆 that line would generate a playlist with this 👇: 
 * best guess track matches for each song on the Spotify playlist

You can see the resulting playlist here: https://tidal.com/browse/playlist/74e2ae5a-e88a-4ac3-8368-ad0235e4bf17

NOTES for using the Spotify flag: 
* It will force `QTY=1` (quantity) so that it only adds one match for each Spotify track
* It will force `AD=1` (allowdupes) so that it (hopefully) has a better quality match (in cases where the Spotify playlist has specific versions or remixes, etc)
* You can supply a full Spotify playlist URL: `https://open.spotify.com/playlist/3cS0NFVjjZlcR7mstctEYT`
* You can supply just the playlist ID: `3cS0NFVjjZlcR7mstctEYT`
* You can supply a Spotify album or artist URL: `https://open.spotify.com/album/6MJb2k5X1k25ebj7ZyixCb`
* You can supply just the back half of a full url: `album/6MJb2k5X1k25ebj7ZyixCb`
* If you supply just an ID, it will be assumed a playlist: `3cS0NFVjjZlcR7mstctEYT` will convert to `playlist/3cS0NFVjjZlcR7mstctEYT` which will convert to the full `https://open.spotify.com/playlist/3cS0NFVjjZlcR7mstctEYT` URL
* Also, I think you can supply multiple, comma-separated Spotify keys, but haven't tested this very well yet

## options

You can view options by running: `python3 tidallister.py --help`

These flags are available:

```
  -h, --help            show this help message and exit
  -A ARTISTS, --artists ARTISTS
                        comma separated list of arists to search for
  -T TRACKS, --tracks TRACKS
                        same as -K, comma separated list of tracks to search for
  -G GENRES, --genres GENRES
                        comma separated list of genres to search for
  -L ALBUMS, --albums ALBUMS
                        comma separated list of albums to search for
  -K KEYWORDS, --keywords KEYWORDS
                        comma separated list, top tracks of each search term
  -S SIMILARS, --similars SIMILARS
                        the number of similar artists to get extra tracks from (only works if
                        -A is declared) (default is 3)
  -SD SIMILARSDEEP, --similarsdeep SIMILARSDEEP
                        use true/false or 1/0, this goes deeper and gets similars of similars
                        (only works if -A & -S are declared) (** BE CAREFUL: this makes your
                        playlist grow exponentially!**)
  -AD ALLOWDUPES, --allowdupes ALLOWDUPES
                        use true/false or 1/0, this allows duplicates if true, default is to
                        skip duplicates
  -P PLAYLIST, --playlist PLAYLIST
                        the name of the playlist to create, optional, will be prefixed with
                        'TidalLister: '
  -Q QTY, --qty QTY     the number of songs from each search to add (default is 10 for each
                        artist/genre/keyword)
  -SP SPOTIFY, --spotify SPOTIFY
                        take a Spotify url (for artist,album,playist) and attempt to recreate
                        it (approximately) in Tidal (forces Q=1 & AD=1)
```

## notes
* **MULTIPLE VERSIONS OF THE SAME SONG BY THE SAME ARTIST**:  By default, the script attempts to prevent duplicates, but this has some holes... When `tidallister` finds a track, it strips out anything in parentheses.  So "Big Hit (2005 Remaster)" and "Big Hit (Live)" would both equal "Big Hit" - to avoid this, try `--allowdupes=1`
* **CONVERT SPOTIFY PLAYLISTS TO TIDAL**: There is an old `spotify-to-tidal.py` script, which just reads a Spotify playlist URL and outputs the command to use for `tidallister.py` - use it like so: `python3 ./spotify-to-tidal.py "http://insert-any-spotify/playlist/url"` but that script is now updated and rolled into the main `tidallister.py` using the `--spotify` flag to supply one or more Spotify urls or playlist IDs
* **MAC APP / APPLESCRIPT GUI**:There is also a `TidalLister.app` folder which is an applescript app that likely won't work on your machine, but i can help you try
