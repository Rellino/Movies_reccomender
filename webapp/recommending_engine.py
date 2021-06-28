"""
This module defines a function that makes predictions based on the 
NFM model which is trained by the recommendation_model.py module.
It also updates the df_final.csv file with new ratings by new users.
"""
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

def get_recommandations(ratings):
    
    # movie-genre matrix
    Q = model.components_  

    # user-genre matrix
    P = model.transform(R)  

    ### Recommendation
    # creating a new user

    new_user = np.full(shape=(1,R.shape[1]), fill_value = df_final.mean().mean())
    
    # THIS PART HAS TO BE UPDATED WITH THE TITLES!!!
    

    new_user[0][15] = ratings['rating1']
    new_user[0][2100] = ratings['rating2']
    new_user[0][65] = ratings['rating3']
    new_user[0][112] = ratings['rating4']
    new_user[0][105] = ratings['rating5']

    #transfering the model for P matrix for the new user
    user_P = model.transform(new_user)

    # getting the actual recommendation by multiplying P and Q
    actual_recommendations = np.dot(user_P, Q) 

    # take a recommendation
    sorted_recomm = np.argsort(actual_recommendations) #index of a sorted array

    # choosing top 5 recommendations 
    top5 = sorted_recomm[:, 0:5].reshape(1*5)
    l_top5 = top5.tolist()


    # Finding the name of recommended movies
    title_list = []
    for i in l_top5:
        title_list.append(MOVIES[MOVIES['movieId']==i].title.iloc[0])

    return title_list


def dataframe_updater():
    pass