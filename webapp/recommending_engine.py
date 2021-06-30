"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This module defines a function that makes predictions based on the 
NFM model which is trained by the recommendation_model.py module.
It also updates the df_final.csv file with new ratings by new users.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import numpy as np
from sklearn.decomposition import NMF
import pandas as pd
import pickle

with open('models/NMF_model.pickle', 'rb') as f:
    model = pickle.load(f)
with open('models/NMF_R.pickle', 'rb') as f2:
    R = pickle.load(f2)


MOVIES = pd.read_csv('../data/raw/movies.csv')

df_final = pd.read_csv('../data/preprocessed/df_final.csv')

def get_recommendations(ratings, titles):
    
    # movie-genre matrix
    Q = model.components_  

    ### Recommendation
    # creating a new user

    new_user = np.full(shape=(1,R.shape[1]), fill_value = df_final.mean().mean())
    
    ids = []
    for title in titles:
        
        ids.append(MOVIES[MOVIES['title']==title]['movieId'].iloc[0])
        
    idx = []
    for movie_id in ids:
        idx.append(df_final.columns.get_loc(str(movie_id)))

    new_user[0][idx[0]] = float(ratings['movie_1'])
    new_user[0][idx[1]] = float(ratings['movie_2'])
    new_user[0][idx[2]] = float(ratings['movie_3'])
    new_user[0][idx[3]] = float(ratings['movie_4'])
    new_user[0][idx[4]] = float(ratings['movie_5'])

    #transfering the model for P matrix for the new user
    user_P = model.transform(new_user)
             
    # getting the actual recommendation by multiplying P and Q
    actual_recommendations = np.dot(user_P, Q) 

    
    # Finding the name of recommended movies
    topn_arr = np.argsort(actual_recommendations[0])[::-1][1:6] 
    
    # top 5 values of the inversely sorted array 
    topn_ind = df_final.columns[topn_arr].tolist() 
    
    # create a list of corresponding ids
    title_list = [MOVIES[MOVIES['movieId']==int(m)]['title'].iloc[0] for m in topn_ind]
    

    
    return title_list, new_user


def dataframe_updater(user):
    df_user = pd.DataFrame(user, columns=df_final.columns)
    df_final_new = df_final.append(df_user, ignore_index=True)
    df_final_new.to_csv('../data/preprocessed/df_final.csv',columns=df_final.columns, index=False)
    