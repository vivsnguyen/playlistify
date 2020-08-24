# <img src="https://github.com/vivsnguyen/playlistify/blob/master/static/images/logo.png" width="40%" alt="Playlistify">

Playlistify creates playlists from your favorite artists' setlists and top songs.

## Deployment
Try it out here: http://playlist-ify.herokuapp.com/
Currently deployed using Heroku.
Previously deployed using AWS and Amazon LightSail.

## Contents
* [Tech Stack](#tech-stack)
* [Features](#features)
* [Future Features](#future)
* [Installation](#installation)

## <a name="tech-stack"></a>Technologies
* Python
* Flask
* Werkzeug
* PostgreSQL
* SQLAlchemy
* HTML
* Jinja
* CSS
* Bootstrap
* JavaScript
* jQuery
* AJAX
* Setlist.FM API
* Spotify Web API
* Spotify Web Playback SDK


## <a name="features"></a>Features

#### Connect to Spotify
Users first connect their Spotify account. Playlistify uses the "Refreshable app authorization" flow, so users only need to connect once per session.

![alt text](https://github.com/vivsnguyen/playlistify/blob/master/static/images/connectToSpotify.gif "Playlistify Spotify User Authentication Redirect")


#### User Login
Users then can log in to their Playlistify account. Passwords are hashed using Werkzeug.

![alt text](https://github.com/vivsnguyen/playlistify/blob/master/static/images/userLogin.gif "Playlistify User Login")

#### User Dashboard
Users can create new playlists, add to existing playlists, listen to existing playlists in browser, or add playlists to their Spotify account.

#### Create a Playlist
Users create a new playlist by providing a title and an artist name. The artist's setlist data is pulled from Setlist.FM to create the playlist.

![alt text](https://github.com/vivsnguyen/playlistify/blob/master/static/images/createPlaylist.gif "Playlistify Create playlist")

#### Add to existing playlist
Users can add to an existing playlist by providing the playlist name and the artist they want to add.

![alt text](https://github.com/vivsnguyen/playlistify/blob/master/static/images/addToPlaylist.gif "Playlistify Add to existing playlist")

#### Play playlist
Users can play, pause, and navigate tracks on their playlists in the browser. The web player functionality is built using the Spotify Web Playback SDK.

![alt text](https://github.com/vivsnguyen/playlistify/blob/master/static/images/playPlaylist.gif "Playlistify play playlists web player")

#### Add playlist to Spotify
Users can add their playlists to Spotify.

![alt text](https://github.com/vivsnguyen/playlistify/blob/master/static/images/addPlaylistToSpotify.gif "Playlistify add playlist to Spotify")

## <a name="future"></a>Future Features
* Display currently playing song
* Autocomplete add to existing playlist
* Autocomplete artist search

## <a name="installation"></a>Installation
To run Playlistify on your own machine:

Clone or fork this repo:
```
https://github.com/vivsnguyen/playlistify.git
```

Create and activate a virtual environment inside your Playlistify directory:
```
virtualenv env
source env/bin/activate
```

Install the dependencies:
```
pip install -r requirements.txt
```

Sign up to use the [Spotify API](https://developer.spotify.com/dashboard/) and [Setlist.FM API](https://www.setlist.fm/settings/apps)

Save your API keys in a file called <kbd>secrets.sh</kbd> using this format:

```
export SETLIST_FM_API_KEY=YOUR_KEY_HERE

export SPOTIPY_CLIENT_ID=YOUR_KEY_HERE

export SPOTIPY_CLIENT_SECRET=YOUR_KEY_HERE
```

Source your keys from your secrets.sh file into your virtual environment:

```
source secrets.sh
```

Set up the database:

```
createdb playlist-creator
python3 model.py
```

Run the app:

```
python3.6 server.py
```

You can now navigate to 'localhost:5000/' to access Playlistify.
