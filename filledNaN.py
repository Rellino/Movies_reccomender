#%%
import numpy as np
from sklearn.decomposition import NMF
import pandas as pd
import matplotlib.pyplot as plt

ratings = pd.read_csv('data/ratings.csv')
movies = pd.read_csv('data/movies.csv')
# %%
ratings.shape, movies.shape, ratings.head(), movies.head()

# %% Made the matrix
user_movie_matrix = pd.pivot_table(ratings, values='rating', index='userId', columns='movieId')
user_movie_matrix

#%%Fill with the averave
user_movie_matrix.mean().mean()
# %% TEST: fill the NaN: with average of the averages:
# print(user_movie_matrix.mean().mean())
# user_movie_matrix.mean(axis=1)


# %%  Fill the matrix:
user_movie_matrix_fin = user_movie_matrix.fillna(user_movie_matrix.mean().mean())
#user_movie_matrix.isna().sum().sum()
# %% look the curve, or not?


# %%
