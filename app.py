from flask import Flask, render_template, session, g, json
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Season, Finish, Race

from helpers import get_data_for_simulator, get_blurbs_for_races

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///influenceF1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)

CURR_USER_KEY = "current_user"


# ***********************************************
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If logged in, add user to Flask global obj."""

    if CURR_USER_KEY in session: 
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def session_login(user):
    """'Log in' user: store user id in session."""

    session[CURR_USER_KEY] = user.id


def session_logout():
    """'Log out' user: delete user id from session."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


# ***********************************************
# Base ROUTING

@app.route('/')
def homepage():
    """Homepage with info and demo of app."""

    return render_template('home.html')


@app.route('/how-it-works')
def tutorial():
    """Tutorial page explaining the app and how the simulator works."""

    return render_template('tutorial.html')


# ***********************************************
# Simulator

@app.route('/simulator/<int:year>')
def simulator(year):
    """Main functionality page of application: show simulator."""

    # is_logged_in()

    #check if season is available, 404 of not
    season = Season.query.get_or_404(year)

    # pass in season year, get back list of 'race labels' and array of driver/finish data objects ("datasets")
    data = get_data_for_simulator(year)
    blurbs = get_blurbs_for_races(year)

    # json information to pass though jinja using |tojson
    json_race_labels = json.dumps(data[0])
    json_datasets = json.dumps(data[1])
    json_blurbs = json.dumps(blurbs)

    return render_template('simulator.html', season=season, race_labels=json_race_labels, datasets=json_datasets, blurbs=json_blurbs)