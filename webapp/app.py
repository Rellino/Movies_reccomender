"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This module controls the workflow of the movie recommender. 
It ties all the other scripts together and produces the web application.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import random
import pandas as pd
from flask import Flask
from flask import render_template
from flask import request
from recommending_engine import get_recommendations, dataframe_updater

MOVIES = pd.read_csv('../data/raw/movies.csv')
df_final = pd.read_csv('../data/preprocessed/df_final.csv')
MOVIE_IDS_LST = df_final.columns.tolist()

app = Flask(__name__)

@app.route('/')
def main_page():
    five_ids = random.sample(MOVIE_IDS_LST,5)
    five_titles = []
    for id in five_ids:
        five_titles.append(MOVIES[MOVIES['movieId']==int(id)]['title'].iloc[0])
    
    return render_template('main.html',
    title='🎬 The Statistically Significant Movie Recommender 🎬',
    subtitle="Courtesy of Laura Bartolini, Behzad Azarhoushang & Francesco Mari,\nwho won't get offended if you don't take their advice (even if you should).",
    movie1=five_titles[0],
    movie2=five_titles[1],
    movie3=five_titles[2],
    movie4=five_titles[3],
    movie5=five_titles[4])


@app.route('/recommender')
def rec_page():
    html_form_data = dict(request.args) # to collect the data from the user (to build the recommendation)
    recs, new_user = get_recommendations(html_form_data) 
    
    dataframe_updater(new_user)

    return render_template('recommender.html', movies = recs)



if __name__ == "__main__":
    app.run(debug=True, port=5000)      


#@movie_app.route('/plot')
# here possible links to the plot under the picture of the recommendation