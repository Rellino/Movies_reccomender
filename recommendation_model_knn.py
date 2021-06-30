#%%
'''
    Item-based Collaborative Filtering for Movie Recommendation System.
    Using KNN with cosine distance
'''
# %%
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import pickle
# %%
# loading the data
ratings = pd.read_csv('data/raw/ratings.csv')
movies = pd.read_csv('data/raw/movies.csv')

# %%
final_dataset = ratings.pivot(index='movieId',columns='userId',values='rating')
final_dataset.head()

#%%
final_dataset.fillna(0,inplace=True)
final_dataset.head()

#%%
csr_data = csr_matrix(final_dataset.values)
final_dataset.reset_index(inplace=True)

# %%
knn = NearestNeighbors(metric='cosine',
                        algorithm='brute',
                        n_neighbors=20,
                        n_jobs=-1)
model = knn.fit(csr_data)

with open('webapp/models/nmf.pickle', 'wb') as f:
    # Pickle the model
    pickle.dump(model, f)

def get_recommendations(movie_name):
    n_movies_to_reccomend = 10
    movie_list = movies[movies['title'].str.contains(movie_name)]  
    if len(movie_list):        
        movie_idx= movie_list.iloc[0]['movieId']
        movie_idx = final_dataset[final_dataset['movieId'] == movie_idx].index[0]
        distances , indices = model.kneighbors(csr_data[movie_idx],n_neighbors=n_movies_to_reccomend+1)    
        rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1])[:0:-1]
        recommend_frame = []
        for val in rec_movie_indices:
            movie_idx = final_dataset.iloc[val[0]]['movieId']
            idx = movies[movies['movieId'] == movie_idx].index
            recommend_frame.append({'Title':movies.iloc[idx]['title'].values[0],'Distance':val[1]})
        df = pd.DataFrame(recommend_frame,index=range(1,n_movies_to_reccomend+1))
        return df
    else:
        return "No movies found. Please check your input"
# %%
get_movie_recommendation('Iron Man')
# %%
get_movie_recommendation('Beautiful Mind')


# %%


# %%
