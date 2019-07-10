# Python Modular Media Server

## Reasoning

Being able to easily publically access your own media shouldn't be a lot to ask for. Plex comes close to my own needs, but the API is poorly documented, the mobile app is far from great, and I'd rather have something open if at all possible. 

My original project, [Plex Music Viewer](https://github.com/JakeStanger/Plex-Music-Viewer), was okay. I personally use it, but I'd imagine the code was pretty hard to follow for anybody else. The API endpoints were a mess. Adding new features began to feel like patching them in rather than developing. 

Rather than trying to modify that project to be what I want, I've decided to start again, and learn from my mistakes. This time I have a plan of attack. Of course the more useful lumps of code will be ported across.

## About

The Python Modular Media Server, or PMMS, as it is currently known, aims to be a fully modular, fully hackable web server. It aims to offer a plugin system which will allow users to add in their own functionality, and modify existing.

Out of the box I plan to include the following functionality:

- API endpoints and database tables for music, movies and television
- Constructing the database from disc, and filewatching to automatically update the database.
- Constructing the database from Plex, and using the events websocket server to sync changes
- Constructing the database from MPD
- Endpoints secured by username/password login where appropriate
- Getting album art from disc, LastFM, MusicBrainz, and Plex.
- Getting lyrics from LyricsGenius
- A static UI, using Flask templates
- A dynamic React UI, using the API
