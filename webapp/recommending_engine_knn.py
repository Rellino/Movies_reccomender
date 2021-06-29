'''
    Item-based Collaborative Filtering for Movie Recommendation System.
    Using KNN with cosine distance
'''
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import pickle



MOVIES = pd.read_csv('../data/raw/movies.csv')
ratings = pd.read_csv('../data/raw/ratings.csv')

final_dataset = ratings.pivot(index='movieId',columns='userId',values='rating')
final_dataset.fillna(0,inplace=True)

csr_data = csr_matrix(final_dataset.values)
final_dataset.reset_index(inplace=True)

with open('models/knn.pickle', 'rb') as f:
    model = pickle.load(f)

def get_recommendations(movie_name):
    n_movies_to_reccomend = 10
    movie_list = MOVIES[MOVIES['title'].str.contains(movie_name)]  
    if len(movie_list):        
        movie_idx= movie_list.iloc[0]['movieId']
        movie_idx = final_dataset[final_dataset['movieId'] == movie_idx].index[0]
        distances , indices = model.kneighbors(csr_data[movie_idx],n_neighbors=n_movies_to_reccomend+1)    
        rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1])[:0:-1]
        recommend_frame = []
        for val in rec_movie_indices:
            movie_idx = final_dataset.iloc[val[0]]['movieId']
            idx = MOVIES[MOVIES['movieId'] == movie_idx].index
            recommend_frame.append(MOVIES.iloc[idx]['title'].values[0])
        return recommend_frame
    else:
        return "No movies found. Please check your input, the first letter of each word should be in Capital letter"



