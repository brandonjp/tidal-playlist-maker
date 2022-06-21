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
                        use true/false or 1/0, this goes deeper and gets similars of similars (only works if -A & -S are
                        declared) (** BE CAREFUL: this makes your playlist grow exponentially!**)
  -P PLAYLIST, --playlist PLAYLIST
                        the name of the playlist to create, optional, will be prefixed with 'TidalLister: '
  -Q QTY, --qty QTY     the number of songs from each search to add (default is 10 for each artist/genre/keyword)
```

## notes
* The script attempts to prevent duplicates, but this has some holes... When `tidallister` finds a track, it strips out anything in parentheses.  So "Big Hit (2005 Remaster)" and "Big Hit (Live)" would both equal "Big Hit"
* **CONVERT SPOTIFY PLAYLISTS TO TIDAL**: There is also a `spotify-to-tidal.py` script, which just reads a Spotify playlist URL and outputs the command to use for `tidallister.py` - use it like so: `python3 ./spotify-to-tidal.py "http://insert-any-spotify/playlist/url"`
* **MAC APP / APPLESCRIPT GUI**:There is also a `TidalLister.app` folder which is an applescript app that likely won't work on your machine, but i can help you try
