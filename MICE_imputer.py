#%%
'''
    It fill the missing rating using MICE imputer method with RF Regressor
    as an estimator.
    Additionally movies with lower than 10 rating and users with less than 
    50 rated movies are deleted from dataset to remove the noises from the data .
'''
#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.ensemble import RandomForestRegressor

#%%[markdown]
### Loading and reshaping the dataset

ratings = pd.read_csv('data/ratings.csv')
movies = pd.read_csv('data/movies.csv')

# %%
ratings.shape, ratings.head(), movies.shape, movies.head()

# %% Made the matrix
df = pd.pivot_table(ratings, values='rating', index='movieId', columns='userId')
df

#%% [markdown]
#### Removing Noise from the data
# * To qualify a movie, a minimum of 10 users should have voted a movie.
# * To qualify a user, a minimum of 50 movies should have voted by the user.
users_rating = ratings.groupby('movieId')['rating'].agg('count')
movies_rating = ratings.groupby('userId')['rating'].agg('count')

# %% Visualization of movies ratings (at least 10 vote per movie as threshold)
f,ax = plt.subplots(1,1,figsize=(16,4))
plt.scatter(users_rating.index,users_rating,color='green')
plt.axhline(y=10,color='r')
plt.xlabel('MovieId')
plt.ylabel('No. of users voted')
plt.show()

#%%
# removing movies below threshold
df_m = df.loc[users_rating[users_rating > 10].index,:]
df_m # The number of movies reduced from 9724 to 2121

#%%
#Visualization of users ratings (at least 50 vote per user as threshold)
f,ax = plt.subplots(1,1,figsize=(16,4))
plt.scatter(movies_rating.index,movies_rating,color='green')
plt.axhline(y=50,color='r')
plt.xlabel('UserId')
plt.ylabel('No. of votes by user')
plt.show()

#%% removing users below threshold
users_threshold = movies_rating[movies_rating > 50]
df_u = df_m.loc[:,movies_rating[movies_rating > 50].index]
df_u # the number of users reduced from 610 to 378
#%%
df_final = df_u.copy()

# %%  Fill the matrix with MICE imputer
imp = IterativeImputer(estimator=RandomForestRegressor(), 
                               initial_strategy='mean',
                               max_iter=10, tol=1e-10, random_state=0)
df_filled = imp.fit_transform(df_final)
df_filled

# %% # Change the numpy ndarray to dataframe
df_clean= pd.DataFrame(data=df_filled[0:,0:],
            index=[i for i in range(df_filled.shape[0])],
            columns=['U_'+str(i) for i in range(df_filled.shape[1])])
df_clean.shape

#%%
# replacing the movieId with ordinal index
df_clean.index = df_filled.index

#%%
# Transposing the matrix X-Axis-> movieID, Y-Axis-> userId
df_final= df_clean.T
df_final

# %% # saving the final df to csv -> Ready for recommender systems
df_final.to_csv('data/df_final.csv', index= False)


