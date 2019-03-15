import sys
import csv
import sqlite3
import spotipy
import spotipy.util as util
import requests as r

# curl -X "GET" "https://api.spotify.com/v1/audio-features/" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer

url='https://accounts.spotify.com/api/BQDD48v7ea2-yFrgmqNxolUdorRoIRQPMCqOsYbQZyMvwwy0asH3zINxDUCHJb5ioNa9te4XeclCKQXBaaXt2NE5BOChdNEUAoJjjOaMd-ehy4ia9-xhKKiCT0575VfuGT1MLcgMR3Vr_biToWophSQ'

#https://api.spotify.com/v1/audio-features/3tddzXTgneWrkV2cYNUBZe

# Create connection to database
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Delete tables if they exist
c.execute('DROP TABLE IF EXISTS "features";')

#Create tables
c.execute('''CREATE TABLE IF NOT EXISTS features(id VARCHAR PRIMARY KEY,
    name VARCHAR, danceability REAL, energy REAL, key REAL, loudness REAL,
    mode REAL, speechiness REAL, acousticness REAL, instrumentalness REAL,
    liveliness REAL, valence REAL, tempo REAL, duration REAL, time_sig REAL);''')
conn.commit()

def grab_features(id):
    sp = spotipy.Spotify()

    #loop through ids
    audio_features = []
    feature = sp.audio_features(id)
    audio_features.append(feature)
    return audio_features


with open('data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        line = row[4].split('/')
        song_id = line[len(line)-1] #string

        #if ID is not already in the table:
            #make API CALL to get the feature values

        song_features = grab_features(song_id)#result of API call

        c.execute('''IF NOT EXISTS (SELECT * FROM features WHERE id = ?)
        BEGIN
            INSERT INTO features VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        END;''', (song_id ,song_id, song_features[0], song_features[1],
        song_features[2], song_features[3], song_features[4], song_features[5], song_features[6], song_features[7],
        song_features[8], song_features[9],song_features[10],song_features[11],song_features[12]))
        conn.commit()

