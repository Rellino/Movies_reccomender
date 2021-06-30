"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Item-based Collaborative Filtering for Movie Recommendation System.
    Using KNN with cosine distance
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors




MOVIES = pd.read_csv('../data/raw/movies.csv')
ratings = pd.read_csv('../data/raw/ratings.csv')



final_dataset = ratings.pivot(index='movieId',columns='userId',values='rating')
final_dataset.fillna(0,inplace=True)

csr_data = csr_matrix(final_dataset.values)
final_dataset.reset_index(inplace=True)

knn = NearestNeighbors(metric='cosine',
                        algorithm="brute",
                        n_neighbors=20,
                        n_jobs=-1)
model = knn.fit(csr_data)



def get_recommendations_knn(movie_name):
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
        return recommend_frame, movie_name
    else:
        lst = [f"🤷🏻‍♀️ Sorry, we could not find “{movie_name}” in our database. Perhaps we don't know it. However...are you SURE that all first letter were capitalised in you imput? 🧐"]
        return lst, movie_name

