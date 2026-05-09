# Tautulli-history-to-ListenBrainz

Recently I found out about ListenBrainz and how it can be somewhat of a recommendation agent for my music listening via PlexAmp with the Weekly Jams playlists but there were a few issues:
1) ListenBrainz did not have my listen history and neither did Spotify or another streamer.
2) There's no native way to give ListenBrainz listen data from Plex or Tautulli.
3) I had no native way to connect my current/future music listening to ListenBrainz.
4) I didn't know how to do any of this, but Google Gemini (free version) was able to get me there with some trial and error.

## Requirments
- Tautulli with listen history.
- Python installed on the machine that will be submitting the listens to ListenBrainz.
- ListenBrainz account.
- SQLite database viewing/querying program (I used DB Browser for SQLite)
- Text editor.

## Listen History
I have been running Tautulli I believe around the time they changed from the name Plexpy. Much longer than I've been using Plex for my music listening, so it had ALL of my Plex listen history. I needed a way to take it from Tautulli and put it into ListenBrainz. Here's what I did if you wanted to replicate what I did:
1) Made a copy of my Taulli database to my local machine. You should probably do this after closing/stopping Tautulli.
2) Open it in a SQLite database reader. I had DB Browser for SQLite already installed from a previous project and for this I'm assuming you are using the same. If not...good luck.
3) Go to the Browse Data tab and select the session_history table.
4) This is going to have every session that Tautulli knows you made. Go to a chunk where you know you were listening to music. You should be able to tell under the product column (it will say Plexamp if you use the app) and the media_type column (this will be track).
5) Once you find sessions you KNOW are music, find the section_id and write that number down (for me this was 5). It will most likely be the same for all the music sessions.
6) Go over to the Execute SQL tab.
7) In the box put the following SQL in but replace whatever section_id with whatever yours is:
     ```
      SELECT 
        m.grandparent_title AS artist_name,
        m.parent_title AS album_name,
        m.title AS track_name,
        h.started AS listened_at
      FROM session_history AS h
      JOIN session_history_metadata AS m ON h.id = m.id
      WHERE h.section_id = 5
      AND m.media_type = 'track'
      ORDER BY h.started DESC;
     ```
     7a) If you want just the results for 1 user add the following after the section_id line and before the media_type line:

         AND h.user = 'YOUR_USERNAME_HERE'

8) Hit the play button or F5 and check the results. It should return the artist's name, album name, track name, and when you listened to the track.
9) If it all looks right then hit the Save the Results View button and then choose Export to CSV. Take the default settings, give it a name, and save it. Make sure you save it in the same folder as you have upload_to_lb.py. We are now done with looking at the database.
10) Open the upload_to_lb.py file in a text editor.
11) On line 6, paste your ListenBrainz token.
    To find your LB Token:
      1) Go to listenbrainz.org.
      2) Sign in.
      3) Go to your Settings.
      4) Hit the Copy button next to User Token.
12) On line 7, paste the name of your CSV file with the extension.
13) Run the python script. `python upload_to_lb.py`
    Make sure you have the python library requests installed.

It could take a while to run. It averages to around 1 listen per second. The script does occasionally take little breaks to not overload the ListenBrainz API.

## Listens going forward
Now that historical data is figured out, we just need to get the future listens into ListenBrainz. This is the easier part on your Plex server spin up a docker container for Multi-Scrobbler (https://docs.multi-scrobbler.app/). I used the following environment variables:
- LZ_USER
- LZ_TOKEN
- PLEX_URL
- PLEX_TOKEN
- PLEX_USERS_ALLOW
- PLEX_LIBRARIES_ALLOW
