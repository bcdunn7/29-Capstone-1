from flask import Flask, render_template, session, g
from flask_debugtoolbar import DebugToolbarExtension

from itertools import groupby

from models import db, connect_db, User, Season, Finish, Race

# from helpers import is_logged_in

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

    season_races = Race.query.filter(Race.season_year == year).all()

    season_races_ids = [race.id for race in season_races]

    season_races_abbrs = [race.abbreviation for race in season_races]
    race_labels = season_races_abbrs.insert(0,'') # first data point will be 'before the season'


    finishes = Finish.query.filter(Finish.race_id.in_(season_races_ids)).all()

    # get useful data from Finishes
    extrapolated_finishes = [(f.race_id, f.driver_id, f.points) for f in finishes]

    # sort finishes to be passed into itertools groupby
    sort_finishes = sorted(extrapolated_finishes, key=lambda fin: fin[1])

    # initialize array to hold groupby results
    driver_finishes_arrays = []

    # group data by driver id
    for key, group in groupby(sort_finishes, lambda fin: fin[1]):
        driver_finishes_arrays.append({'label': key, 'data': list(group)})

    

    print(driver_finishes_arrays)

    return render_template('simulator.html', race_labels=race_labels)