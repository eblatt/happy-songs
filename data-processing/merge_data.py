import sqlite3

conn = sqlite3.connect('data.db')
conn.text_factory = str
c = conn.cursor()

# if change made, must drop the table and re-add it
# c.execute('DROP TABLE IF EXISTS hcc')
# c.execute('DROP TABLE IF EXISTS sf')
# c.execute('DROP TABLE IF EXISTS sh')

#happiness table with country codes
c.execute('''CREATE TABLE IF NOT EXISTS hcc AS
              SELECT happiness.country_name,
                     country_codes.country_code,
                     happiness.rank,
                     happiness.score,
                     happiness.high,
                     happiness.low,
                     happiness.gdp,
                     happiness.fam,
                     happiness.health,
                     happiness.freedom,
                     happiness.gen,
                     happiness.trust,
                     happiness.dys
              FROM   happiness
                     INNER JOIN country_codes
                             ON happiness.country_name = country_codes.country_name''')

#songs table with features
c.execute('''CREATE TABLE IF NOT EXISTS sf AS
              SELECT songs.songid,
                     songs.track,
                     songs.artist,
                     songs.region,
                     songs.datee,
                     songs.position,
                     songs.streams,
                     features.danceability,
                     features.energy,
                     features.key,
                     features.loudness,
                     features.mode,
                     features.speechiness,
                     features.acousticness,
                     features.instrumentalness,
                     features.liveness,
                     features.valence,
                     features.tempo,
                     features.duration,
                     features.time_sig
              FROM   songs
                     INNER JOIN features
                             ON songs.songid = features.id''')

#final table sf with hcc
c.execute('''CREATE TABLE IF NOT EXISTS sh AS
              SELECT sf.songid,
                     sf.track,
                     sf.artist,
                     sf.region,
                     sf.datee,
                     sf.position,
                     sf.streams,
                     sf.danceability,
                     sf.energy,
                     sf.key AS song_key,
                     sf.loudness,
                     sf.mode,
                     sf.speechiness,
                     sf.acousticness,
                     sf.instrumentalness,
                     sf.liveness,
                     sf.valence,
                     sf.tempo,
                     sf.duration,
                     sf.time_sig,
                     hcc.country_name,
                     hcc.rank,
                     hcc.score,
                     hcc.high,
                     hcc.low,
                     hcc.gdp,
                     hcc.fam,
                     hcc.health,
                     hcc.freedom,
                     hcc.gen,
                     hcc.trust,
                     hcc.dys
              FROM   sf
                     JOIN hcc
                       ON sf.region = hcc.country_code''')

conn.commit()
conn.close()
