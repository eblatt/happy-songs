import json
import csv
import sqlite3

songs = {}
country_codes = {}
happiness = {}

def open_csv_songs(csv_file):
	with open(csv_file) as f:
		reader = csv.DictReader(f)
		for row in reader:
			if row['Date'].split("-")[0] == '2017':
				split = row['URL'].split('/')
				spotify_id = split[len(split)-1]
				songs[spotify_id] = row # 'Artist', 'URL', 'Region', 'Date', 'Streams', 'Track Name', 'Position'

def open_csv_country(csv_file):
	with open(csv_file) as f:
		reader = csv.DictReader(f)
		for row in reader:
			#removing certain country prefixes
			country_name = row['Name'].split(",")[0]
			country_code = row['Code']
			#special cases
			if(country_code == 'cg'):
				country_name = "Congo (Brazzaville)"
			if(country_code == 'cd'):
				country_name = "Congo (Kinshasa)"
			# print(country_name, country_code)
			country_codes[country_code] = country_name

def open_csv_world_happiness(csv_file):
	with open(csv_file) as f:
		reader = csv.DictReader(f)
		for row in reader:
			country_name = row['Country']
			# rank = info['Happiness.Rank']
			# score = info['Happiness.Score']
			# high = info['Whisker.high']
			# low = info['Whisker.low']
			# gdp = info['Economy..GDP.per.Capita']
			# fam = info['Family']
			# health = info['Health..Life.Expectancy']
			# freedom = info['Freedom']
			# gen = info['Generosity']
			# trust = info['Trust..Government.Corruption']
			# dys = info['Dystopia.Residual']
			row.pop('Country')
			happiness[country_name] = row

def main():
	open_csv_songs("spotify-worldwide-daily.csv")
	open_csv_country("country_codes.csv")
	open_csv_world_happiness("world_happiness_2017.csv")
	conn = sqlite3.connect('data.db')
	conn.text_factory = str
	c = conn.cursor()

	# if change made, must drop the table and re-add it
	c.execute('DROP TABLE IF EXISTS songs')
	c.execute('DROP TABLE IF EXISTS country_codes')
	c.execute('DROP TABLE IF EXISTS happiness')

	#Spotify's Worldwide Daily Song Ranking
	c.execute('''CREATE TABLE IF NOT EXISTS songs(
			     songid   VARCHAR NOT NULL,
			     artist   VARCHAR NOT NULL,
			     region   VARCHAR NOT NULL,
			     datee    VARCHAR NOT NULL,
			     position VARCHAR NOT NULL,
			     PRIMARY KEY(songid)
			  )''')

	#countries with their 2 digit codes
	c.execute('''CREATE TABLE IF NOT EXISTS country_codes(
			     country_code   VARCHAR NOT NULL,
			     country_name   VARCHAR NOT NULL,
			     PRIMARY KEY(country_code)
			  )''')

	#World Happiness Report
	c.execute('''CREATE TABLE IF NOT EXISTS happiness(
			     country_name VARCHAR NOT NULL,
			     rank         INTEGER NOT NULL,
			     score        REAL NOT NULL,
			     high         REAL NOT NULL,
			     low          REAL NOT NULL,
			     gdp          REAL NOT NULL,
			     fam          REAL NOT NULL,
			     health       REAL NOT NULL,
			     freedom      REAL NOT NULL,
			     gen          REAL NOT NULL,
			     trust        REAL NOT NULL,
			     dys          REAL NOT NULL,
			     PRIMARY KEY(country_name)
			  )''')

	#insert data to tables
	for song_id, info in songs.items():
		c.execute('INSERT INTO songs VALUES(?,?,?,?,?)', (song_id, info['Artist'], info['Region'], info['Date'],  info['Position']))
	for country_code, country_name in country_codes.items():
		c.execute('INSERT INTO country_codes VALUES (?,?)', (country_code, country_name))
	for country_name, info in happiness.items():
		c.execute('INSERT INTO happiness VALUES(?,?,?,?,?,?,?,?,?,?,?,?)', (country_name, info['Happiness.Rank'], info['Happiness.Score'], info['Whisker.high'], info['Whisker.low'], info['Economy..GDP.per.Capita.'], info['Family'], info['Health..Life.Expectancy.'], info['Freedom'], info['Generosity'], info['Trust..Government.Corruption.'], info['Dystopia.Residual']))

	#commit changes and close
	conn.commit()
	conn.close()

main()
