""" Identifiers that can be used to link to other sources of movie data are contained in the file `links.csv`. Each line of this file after the header row represents one movie, and has the following format:
    movieId,imdbId,tmdbId
movieId is an identifier for movies used by <https://movielens.org>. E.g., the movie Toy Story has the link <https://movielens.org/movies/1>.

imdbId is an identifier for movies used by <http://www.imdb.com>. E.g., the movie Toy Story has the link <http://www.imdb.com/title/tt0114709/>.

tmdbId is an identifier for movies used by <https://www.themoviedb.org>. E.g., the movie Toy Story has the link <https://www.themoviedb.org/movie/862>.

"""

# First do a merge of the table and take only the common MovieId

#%%
import pandas as pd
import requests
from bs4 import BeautifulSoup as soup

#%% read the movie-link and the final table:
links = pd.read_csv('../data/raw/links.csv')
df_final = pd.read_csv('../data/preprocessed/df_final.csv')

#%% The index of df_final was a string convert it and make new df called fin_df
dfdf = df_final.T
fin_df = dfdf.index.astype(int, copy=True)
fin_df
# print(df_final.index)
#%%
type(fin_df)
#%% add a new colum called movieId (it was already there but not as a coulm)
dfdf['movieId']=fin_df
dfdf
#%% #Merge the table and the complate df into one
merged_df = pd.merge(links, dfdf, on=['movieId'])
merged_df
#take only the relevant colums
links_df = superdf.loc[:,['movieId', 'imdbId', 'tmdbId']]
links_df
# %% 
response = requests.get('http://www.imdb.com/title/tt0114709/')
response
# %%
web_html = soup(response.text)
# %%
web_html.find('img', )