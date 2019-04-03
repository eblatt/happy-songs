import sys
import csv
import sqlite3
import spotipy
import spotipy.util as util
import requests
import json
#from requests_oauthlib import OAuth1

# Create connection to database
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Delete tables if they exist
c.execute('DROP TABLE IF EXISTS "features";')

#Create tables
c.execute('''CREATE TABLE IF NOT EXISTS features(id VARCHAR PRIMARY KEY,
    danceability REAL, energy REAL, key REAL, loudness REAL,
    mode REAL, speechiness REAL, acousticness REAL, instrumentalness REAL,
    liveness REAL, valence REAL, tempo REAL, duration REAL, time_sig REAL);''')
conn.commit()

#0 - ID
#1 - name - dont have yet // DONT NEED ANYMORE
#2 - danceability 8
#3 - energy 2
#4 - key 0
#5 - loudness 11
#6 - mode 12
#7 - speechiness 5
#8 - acousticness 7
#9 - instrumentalness 16
#10 - liveness 3
#11 - valence 13
#12 - tempo 4
#13 - duration 10
#14 - time_sig 9


def grab_features(ids):

    sp = spotipy.Spotify(auth='BQDZReErZM5jAZGP-BYQ_NQWqT76J1WaLyUXcsc_yRk8bgxcrrM0-8lwBj1XaEp1rYgbLXp3vOhRG8LStJRBHvgKVHcn3hAbiyKNVLWIpqw_zPqE6FvCLKK07MaS5nkSMtgM6TPLM8gt4BJEpzzXgy0')
#
#    #check 200 status code
#

    song_set = sp.audio_features(ids) #len 50

    feature_set = []
    for song in song_set:
        if song is not None:
            c.execute('''INSERT INTO features (id,
                danceability, energy, key, loudness,
                mode, speechiness, acousticness, instrumentalness,
                liveness, valence, tempo, duration, time_sig)
                SELECT ?,?,?,?,?,?,?,?,?,?,?,?,?,?
                WHERE NOT EXISTS (SELECT * FROM features WHERE id = ?)''', (song['id'], song['danceability'], song['energy'], song['key'], song['loudness'], song['mode'], song['speechiness'], song['acousticness'], song['instrumentalness'], song['liveness'], song['valence'], song['tempo'], song['duration_ms'], song['time_signature'], song['id']))
            conn.commit()
        else:
            print("Song is Null:", song)
    return feature_set #list of lists. length 50. each sublist has features of each song

with open('data.csv') as csv_file:
    data = list(csv.reader(csv_file, delimiter=','))
    line_count = 0
    ids = []
    feature_set = []
    
    for row in range(1, len(data), 10): #start doing the skips at this level
        line = data[row][4].split('/')
        song_id = line[len(line)-1] #string
        
        if song_id and len(song_id) == 22:
            line_count += 1
            if line_count % 20 == 1: #every 20
                ids.append(song_id)
        else:
            print("not valid:", song_id)
    
        #also update to 100 at a time
        if line_count == 100:
            feature_set = grab_features(ids)
            ids = []
            line_count = 0

    #if there isn't 100 at the end, read the last few songs
    feature_set = grab_features(ids)

#song_features = []
#            song_features.extend((song['id'], name, song['danceability'], song['energy'], song['key'], song['loudness'], song['mode'], song['speechiness'], song['acousticness'], song['instrumentalness'], song['liveness'], song['valence'], song['tempo'], song['duration_ms'], song['time_signature']))
#feature_set.append(song_features)
#if ID is not already in the table:

#    #50 at a time
#    counter = 0
#    while counter < len(ids):
#
#        song_features = grab_features(ids) #result of API call


#        c.execute('''IF NOT EXISTS (SELECT * FROM features WHERE id = ?)
#        BEGIN INSERT INTO features VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?) END;''', (song_features[0], song_features[0], song_features[1], song_features[2], song_features[3], song_features[4], song_features[5], song_features[6], song_features[7],song_features[8], song_features[9], song_features[10], song_features[11], song_features[12], song_features[13], song_features[14]))
#        conn.commit()




