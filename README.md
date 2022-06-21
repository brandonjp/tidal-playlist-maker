# tidal-playlist-maker
TidalLister - command line python script that will generate a Tidal playlist from input such as artist, album, genre, keyword, etc.

## usage
`python3 ./tidallister.py -A "Harry Nilsson, Amy Grant" -L "Bringing Down the Horse" -G "Jazz" -K "piano cover" -Q "5"`

👆 This would generate a playlist with: 
 * 5 songs from the artist Harry Nilsson
 * 5 songs from the artist Amy Grant
 * all songs from the album Bringing Down the Horse
 * 5 songs in the Jazz genre
 * 5 songs matching the keyword phrase "piano cover"

You can see the resulting playlist here:  http://tidal.com/browse/playlist/8fbc08ab-6f76-41fb-97df-60f0bff4095f

## options

You can view options by running: `python3 tidallister.py --help`

These flags are available:

```
  -h, --help            show this help message and exit
  -A ARTISTS, --artists ARTISTS
                        comma separated list of arists to search for
  -G GENRES, --genres GENRES
                        comma separated list of genres to search for
  -L ALBUMS, --albums ALBUMS
                        comma separated list of albums to search for
  -K KEYWORDS, --keywords KEYWORDS
                        comma separated list, top tracks of each search term
  -S SIMILARS, --similars SIMILARS
                        the number of similar artists to get extra tracks from (only works if -A is declared) (default is
                        3)
  -SD SIMILARSDEEP, --similarsdeep SIMILARSDEEP
                        go deeper and get similars of similars (only works if -A -S is declared) (** BE CAREFUL: this
                        makes your playlist grow exponentially!**)
  -P PLAYLIST, --playlist PLAYLIST
                        the name of the playlist to create, optional, will be prefixed with 'TidalLister: '
  -Q QTY, --qty QTY     the number of songs from each search to add (default is 10 for each artist/genre/keyword)
```

## notes
* The script attempts to prevent duplicates, but this has some holes... When `tidallister` finds a track, it strips out anything in parentheses.  So "Big Hit (2005 Remaster)" and "Big Hit (Live)" would both equal "Big Hit"
* **CONVERT SPOTIFY PLAYLISTS TO TIDAL**: There is also a `spotify-to-tidal.py` script, which just reads a Spotify playlist URL and outputs the command to use for `tidallister.py` - use it like so: `python3 ./spotify-to-tidal.py "http://insert-any-spotify/playlist/url"`
* **MAC APP / APPLESCRIPT GUI**:There is also a `TidalLister.app` folder which is an applescript app that likely won't work on your machine, but i can help you try
