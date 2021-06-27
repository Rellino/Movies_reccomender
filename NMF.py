#%%
''' 
    Building a Movie Recommendation Model Using NMF.
'''
# %%
import numpy as np
from numpy.core.fromnumeric import sort
from sklearn.decomposition import NMF
import pandas as pd
import pickle
# %%
# Loading the preprocess rating file
# X-Axis -> userId , Y-Axis -> movieId
df_final = pd.read_csv('data/df_final.csv')
movies = pd.read_csv('data/movies.csv')
df_final

# %% 
# Changing dataframe to numpy ndarray for building R matrix 
R = pd.DataFrame(df_final, index=df_final.index, columns=df_final.columns).values

# %%
#create a model and set the hyperparameters
# 20 Genres (from EDA.py) + 106 years -> 126 number of components
model = NMF(n_components=126, init='random', random_state=1, max_iter=100000, solver='cd')

# fitting the model to R
model.fit(R)

# movie-genre matrix
Q = model.components_  

# user-genre matrix
P = model.transform(R)  

#%%
# saving the model
filename = 'finalized_NMF_model.sav'
pickle.dump(model, open(filename, 'wb')) 

# %%[markdown]
### Recommendation
# %%
# creating a new user
new_user = np.full(shape=(1,R.shape[1]), fill_value = df_final.mean().mean())

# %%
# asking the user to predict 3 movies randomly
new_user[0][30] = 1
new_user[0][15] = 3
new_user[0][2100] = 5

# %%
#transfering the model for P matrix for the new user
user_P = model.transform(new_user)

# getting the actual recommendation by multiplying P and Q
actual_recommendations = np.dot(user_P, Q) 

# take a recommendation
sorted_recomm= np.argsort(actual_recommendations) #index of a sorted array

# choosing top 5 recommendations 
top5 = sorted_recomm[:, 0:5].reshape(1*5)
top5= top5.tolist()
top5

# %%
# Finding the name of recommended movies
for i in top5:
    name = movies[movies['movieId']==i].title.iloc[0]
    print(name)
