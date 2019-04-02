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
    name VARCHAR, danceability REAL, energy REAL, key REAL, loudness REAL,
    mode REAL, speechiness REAL, acousticness REAL, instrumentalness REAL,
    liveness REAL, valence REAL, tempo REAL, duration REAL, time_sig REAL);''')
conn.commit()

#0 - ID
#1 - name - dont have yet
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

    sp = spotipy.Spotify(auth='BQCb3w75TyqNhZ3P1ct8gkLvlukfCkwdSqPmolsIrhrNyOPBSoBDvyaQ8QPMQ9qXat7JGHqmWSN3_JyvT3vyD8FDdlAZXRZQQSNmlKyv_6JeqQoANCdztZUzoW0z-IO0au4ENXNZWA42jeENurrShNs')
#
#    #check 200 status code
#

    song_set = sp.audio_features(ids) #len 50

    feature_set = []
    for song in song_set:
        song_features = []
        name = 'placeholder'
        song_features.extend((song['id'], name, song['danceability'], song['energy'], song['key'], song['loudness'], song['mode'], song['speechiness'], song['acousticness'], song['instrumentalness'], song['liveness'], song['valence'], song['tempo'], song['duration_ms'], song['time_signature']))
        feature_set.append(song_features)
    return feature_set #list of lists. length 50. each sublist has features of each song

#    feature_set = []
#
#    for i in range(10):
#        song_features = []
#        features = sp.audio_features(ids[i]) #sample '2ekn2ttSfGqwhhate0LSR0' this line causes id to change to "URL" and my access token keeps expiring
#        features = json.dumps(features[0])
#        features = json.loads(features)
#        name = 'placeholder'
#        song_features.extend((ids[i], name, features['danceability'], features['energy'], features['key'], features['loudness'], features['mode'], features['speechiness'], features['acousticness'], features['instrumentalness'], features['liveness'], features['valence'], features['tempo'], features['duration_ms'], features['time_signature']))
#        feature_set.append(song_features)
#    print(feature_set)
#    return feature_set


with open('data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    ids = []

    for row in csv_reader:
        line = row[4].split('/')
        #print(line)
        song_id = line[len(line)-1] #string

        #if ID is not already in the table:
            #make API CALL to get the feature values
            #print(song_id) #WHY IS IT GETTING CHANGED TO URL???
        if not song_id == 'URL':
            ids.append(song_id)

        line_count += 1
        if line_count == 50:
            feature_set_50 = grab_features(ids)
            for song_features in feature_set_50:
                c.execute('''INSERT INTO features (id,
                    name, danceability, energy, key, loudness,
                    mode, speechiness, acousticness, instrumentalness,
                    liveness, valence, tempo, duration, time_sig)
                    SELECT ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
                    WHERE NOT EXISTS (SELECT * FROM features WHERE id = ?)''', (song_features[0], song_features[1], song_features[2], song_features[3], song_features[4], song_features[5], song_features[6], song_features[7],song_features[8], song_features[9], song_features[10], song_features[11], song_features[12], song_features[13], song_features[14], song_features[0]))
                conn.commit()
            ids = []
            line_count = 0
            #print("new 50")





#    #50 at a time
#    counter = 0
#    while counter < len(ids):
#
#        song_features = grab_features(ids) #result of API call


#        c.execute('''IF NOT EXISTS (SELECT * FROM features WHERE id = ?)
#        BEGIN INSERT INTO features VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?) END;''', (song_features[0], song_features[0], song_features[1], song_features[2], song_features[3], song_features[4], song_features[5], song_features[6], song_features[7],song_features[8], song_features[9], song_features[10], song_features[11], song_features[12], song_features[13], song_features[14]))
#        conn.commit()




