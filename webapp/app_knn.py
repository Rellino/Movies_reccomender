"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This module controls the workflow of the movie recommender. 
It ties all the other scripts together and produces the web application.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from flask import Flask
from flask import render_template
from flask import request
from recommending_engine import get_recommendations


app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('main.html', title='Francesco e Laura')


@app.route('/recommender')
def rec_page():
    html_form_data = request.args['rating1'] # to collect the data from the user (to build the recommendation)
    print(html_form_data)
    recs = get_recommendations(html_form_data) 
    
    return render_template('recommender.html', movies = recs)



if __name__ == "__main__":
    app.run(debug=True, port=5000)      


#@movie_app.route('/plot')
# here possible links to the plot under the picture of the recommendation