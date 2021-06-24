#%%
# stupid recommender
import pandas as pd
import random

list_movie = pd.read_csv('../data/movies.csv')
movie_list = list(list_movie['title'])
#print(movie_list)

def get_recommendations():
    random.shuffle(movie_list)
    return movie_list[:5]
# %%
print(get_recommendations())
# %%
