import json
import csv
import sqlite3

songs = {}

def open_csv(csv_file):
	with open(csv_file) as f:
		reader = csv.DictReader(f)
		print(reader)
		for row in reader:
			# print(row['URL'].split('/')[4])
			if row['Date'].split("-")[0] == '2017':
				split = row['URL'].split('/')
				spotify_id = split[len(split)-1]
				songs[spotify_id] = row # 'Artist', 'URL', 'Region', 'Date', 'Streams', 'Track Name', 'Position'
			# print(row[0])


def main():
	print("hi")
	open_csv("spotify-worldwide-daily.csv")
	conn = sqlite3.connect('data.db')
	conn.text_factory = str

	c = conn.cursor()
	c.execute('DROP TABLE IF EXISTS "songs"')
	c.execute('CREATE TABLE songs(songid VARCHAR not null, artist VARCHAR not null, region VARCHAR not null, datee VARCHAR not null, position VARCHAR not null, PRIMARY KEY(songid))')
	for song_id, info in songs.items():
		c.execute('INSERT INTO songs VALUES(?,?,?,?,?)', (song_id, info['Artist'], info['Region'], info['Date'],  info['Position'] ))
	conn.commit()
main()
# '''

# Input: JSON file
# Output: dictionary that uses the titles as keys and book descriptions as values

# '''
# def make_book_dict(json_file):
# 	book_dict = {}

# 	json_data = json.load(open(json_file))
# 	for element in json_data:
# 		title = element["title"]
# 		book_dict[title] = element["description"]

# 	return book_dict

# '''

# Input: CSV file
# Output: dictionary with keywords as keys and associated genres and points as the values

# '''
# def make_keyword_dict(csv_file):
# 	keyword_dict = {}

# 	with open(csv_file) as f:
# 		reader = csv.DictReader(f)
# 		for row in reader:
# 			keyword = row[" Keyword"].lstrip() 
# 			genre = row["Genre"]
# 			points = int(row[" Points"])
# 			if keyword not in keyword_dict:
# 				keyword_dict[keyword] = [(genre, points)]
# 			else:
# 				keyword_dict[keyword].append((genre, points))

# 	return keyword_dict

# '''
# Input: JSON file and CSV file
# Output: The title of the book and the three highest genres based on keywords in the desctiption
# '''
# def make_genres(json_file,csv_file):
	
# 	'''
# 	Initially, I read all the data from the JSON and csv files, 
# 	and put the info into dictionaries so that it is easier to interpret
# 	the data.
# 	'''

# 	book_dict = make_book_dict(json_file) # book: description
# 	keyword_dict = make_keyword_dict(csv_file) #keyword: [(genre,points)]
# 	books_and_genres = {} #title: [(genre, points for every new word, number of keywords found, number of new keywords found)]
# 	new_genre = True 
	

# 	# for each title, I find the keywords and then add the value of the keywords together
# 	for title in book_dict.keys():		
# 		description = book_dict[title]
# 		visited_kw = set()
# 		for keyword in keyword_dict.keys():
# 			x = description.find(keyword)
# 			while (x != -1):
# 				x = description.find(keyword,x+len(keyword)) # finding the keyword
# 				for (genre,points) in keyword_dict[keyword]:
# 					if title not in books_and_genres.keys():
# 						books_and_genres[title] = [(genre, points,1,1)] #adding to dictionary
# 					else:
# 						# adding additional genres to the dictionary
# 						for (prev_genre,prev_pts,hits,avg) in books_and_genres[title]:
# 							#if the keyword is for a genre that has already been matched, just keep adding
# 							if genre == prev_genre:
# 								if keyword not in visited_kw:
# 									books_and_genres[title].append((genre,prev_pts+points, hits+1,avg+1))
# 									books_and_genres[title].remove((genre,prev_pts,hits,avg))
# 									new_genre = False
# 									break
# 								else:
# 									books_and_genres[title].append((genre,prev_pts, hits+1,avg))
# 									books_and_genres[title].remove((genre,prev_pts,hits,avg))
# 									new_genre = False
# 									break
# 						# otherwise, add to the dictionary
# 						if new_genre is True:
# 							books_and_genres[title].append((genre, points, 1,1))
# 							new_genre = True
# 				visited_kw.add(keyword)

# 	#alphabetic order and top three genres
# 	for book_title in sorted(books_and_genres.keys()):
# 		print(book_title)
# 		sorted_genres = {}
# 		max_pts = float("-inf")
# 		l =[]
# 		for info in books_and_genres[book_title]:
# 			(genre,points,hits,avg) = info
# 			score = (points/avg)*hits
# 			sorted_genres[score] = genre
# 			l.append(score)
# 			counter = 0 
# 			while l and counter < 3 :
# 				max_score = max(l)
# 				print((sorted_genres[max_score],max_score))
# 				l.remove(max_score)
# 				counter+=1
			


# def main():                      
#    make_genres("sample_book_json.txt","sample_genre_keyword_value.csv")

# main() 








