import pandas as pd
import json

df = pd.read_csv('movies_initial.csv')

df.to_json('movies.json', orient='records')

with open('movies.json', 'r') as json_file:
    movies = json.load(json_file)

for movie in movies:
    print(movie)
    break

