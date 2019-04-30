import json
import csv
import sqlite3

country_loc= {}
def open_csv_country_two(csv_file):
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            country_name = row['CountryName']
            cc = row['CountryCode']
            country_loc[cc] = row

def main():
    open_csv_country_two("country-capitals.csv")
    conn = sqlite3.connect('data.db')
    conn.text_factory = str
    c = conn.cursor()

    # Delete tables if they exist
    c.execute('DROP TABLE IF EXISTS "country_loc";')

    # if change made, must drop the table and re-add it
    # c.execute('DROP TABLE IF EXISTS country_loc')

    #Country information, including latitude and longitude
    c.execute('''CREATE TABLE IF NOT EXISTS country_loc(
    		     country_name VARCHAR NOT NULL,
    		     cap_name     VARCHAR NOT NULL,
    		     cap_lat      REAL NOT NULL,
    		     cap_long     REAL NOT NULL,
    		     cc           VARCHAR NOT NULL,
    		     continent    VARCHAR NOT NULL,
    		     PRIMARY KEY(cc)
    		  )''')

    #insert data to table
    for cc, info in country_loc.items():
    	c.execute('INSERT OR IGNORE INTO country_loc VALUES (?,?,?,?,?,?)', (info['CountryName'], info['CapitalName'], info['CapitalLatitude'], info['CapitalLongitude'], cc, info['ContinentName']))
    #commit changes and close
    conn.commit()
    conn.close()

main()
