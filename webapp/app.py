"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This module controls the workflow of the movie recommender. 
It ties all the other scripts together and produces the web application.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import re
from flask import Flask         
from flask import render_template   
#from recommender import get_recommendations   
from flask import request

movie_app = Flask(__name__)

@movie_app.route('/')
def main_page():
    return render_template('main.html')



@movie_app.route('/recommender')
def rec_page():
    return render_template('recommender.html')











if __name__ == "__main__":
    movie_app.run(debug=True, port=5000)      