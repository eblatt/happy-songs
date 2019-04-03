# Happy Hits | Turn Up Tunes | Juicy Jams

What song features predict happiness of a country? What song features are more popular/are liked the most by the happiest countries?

In this project, we plan to merge data on happiness by country and top Spotify songs per country from 2017 in order to answer these questions. So far, we've worked on merging the data based on country code. We plan to use a random sample of about 25 of the top 200 songs from a select number of countries, in order to cut down on some of the data. We will implement a supervised learning algorithm for our predictions and find correlations between happier countries and higher values of certain song features. We may use this data to do a sentiment analysis of top songs by region and measure how consistent it is with our happiness data. We eventually plan to present this data in a map-like visualization.


Raw:

data.db- In this file, we have the database of every region's 200 top songs for every day for the year 2017. We plan to add information regarding the audio features of each song to this database by using Spotify's API. We found the data at https://www.kaggle.com/edumucelli/spotifys-worldwide-daily-song-ranking/version/3. 

world_happiness_report.csv- In this file, we have the happiness rankings of 155 countries. We found the data at https://www.kaggle.com/unsdsn/world-happiness. 

country_codes.csv = In this file, we have country names along with their country codes. We found the data at https://datahub.io/core/country-list#resource-country-list_zip
