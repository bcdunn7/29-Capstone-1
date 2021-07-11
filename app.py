from flask import Flask, render_template, session, g, json, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Season, Finish, Race

from forms import UserForm

from helpers import get_data_for_simulator, get_blurbs_for_races, get_changes_data

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
# Users
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user signup.
    
    On get, show form for user signup.
    
    On post, create new user and add to DB and redirect to home. """

    form = UserForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data
            )
            db.session.commit()
        except IntegrityError:
            flash("Username already taken", "warning")
            return render_template('users/signup.html', form=form)

        session_login(user)
        flash("Welcome!", "info")
        return redirect('/')
    
    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Log in user."""

    form = UserForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            session_login(user)
            flash(f"Welcome back, {user.username}", "info")
            return redirect('/')
        else:
            flash("Invalid credentials", "danger")

    return render_template('users/login.html', form=form)


@app.route('/logout', methods=['POST'])
def logout():
    """Logout user"""

    session_logout()

    flash("Successfully logged out.", "info")

    return redirect('/')


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
    changes = get_changes_data(year)

    # json information to pass though jinja using |tojson
    json_race_labels = json.dumps(data[0])
    json_datasets = json.dumps(data[1])
    json_blurbs = json.dumps(blurbs)
    json_change_texts = json.dumps(changes[0])
    json_changes = json.dumps(changes[1])

    return render_template('simulator.html', season=season, race_labels=json_race_labels, datasets=json_datasets, blurbs=json_blurbs, change_texts=json_change_texts, changes=json_changes)