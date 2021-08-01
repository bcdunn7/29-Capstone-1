import os

from flask import Flask, render_template, session, g, json, flash, redirect, request
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Season, User_Change, Race

from forms import UserForm

from helpers import not_logged_in, logged_in, get_data_for_simulator, get_blurbs_for_races, get_changes_data, get_user_changes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///influenceF1'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret')

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


@app.errorhandler(404)
def page_not_found(e):
    """Custom 404."""

    return render_template('404.html'), 404


# ***********************************************
# Users
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user signup.
    
    On get, show form for user signup.
    
    On post, create new user and add to DB and redirect to home. """

    if (logged_in()):
        return redirect('/')

    form = UserForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data
            )
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username Already Taken')
            return render_template('users/signup.html', form=form)

        session_login(user)
        flash("Welcome!", "info")
        return redirect('/')
    
    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Log in user."""

    if (logged_in()):
        return redirect('/')

    form = UserForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            session_login(user)
            flash(f"Welcome back, {user.username}", "info")
            return redirect('/')
        else:
            form.username.errors.append("Invalid Credentials")
            form.password.errors.append("Invalid Credentials")

    return render_template('users/login.html', form=form)


@app.route('/logout', methods=['POST'])
def logout():
    """Logout user"""

    session_logout()

    flash("Successfully logged out.", "info")

    return redirect('/')


@app.route('/profile')
def show_profile():
    """Profile page for user."""

    if (not_logged_in()):
        return redirect('/login')

    return render_template('users/profile.html')


@app.route('/profile', methods=['POST'])
def delete_user():
    """Deletes and log out user."""

    session_logout()

    User.query.filter(User.id == g.user.id).delete()
    db.session.commit()

    flash("User Successfully Deleted", "success")

    return redirect('/')


@app.route('/erase', methods=['POST'])
def delete_user_data():
    """Delete stored User_Changes for given user."""

    User_Change.query.filter(User_Change.user_id == g.user.id).delete()
    db.session.commit()

    flash("Data Deleted", "info")

    return redirect('/profile')


# ***********************************************
# Simulator

@app.route('/simulator/<int:year>')
def simulator(year):
    """Main functionality page of application: show simulator."""

    if (not_logged_in()):
        return redirect('/login')
    
    #check if season is available, 404 of not
    season = Season.query.get_or_404(year)

    # pass in season year, get back list of 'race labels' and array of driver/finish data objects ("datasets"), toggle options, and preset toggles
    data = get_data_for_simulator(year)
    blurbs = get_blurbs_for_races(year)
    changes = get_changes_data(year)
    user_changes = get_user_changes(year)

    # json information to pass though jinja using |tojson
    json_race_labels = json.dumps(data[0])
    json_datasets = json.dumps(data[1])
    json_blurbs = json.dumps(blurbs)
    json_change_texts = json.dumps(changes[0])
    json_changes = json.dumps(changes[1])
    json_user_changes = json.dumps(user_changes)

    return render_template('simulator.html', season=season, race_labels=json_race_labels, datasets=json_datasets, blurbs=json_blurbs, change_texts=json_change_texts, changes=json_changes, user_changes=json_user_changes)


# Accept JSON info and save to DB
@app.route('/simulator/save', methods=['POST'])
def save_toggles():
    """Accepts a json array of race_ids and saves user/race connections to db."""

    if (not_logged_in()):
        return redirect('/login')

    race_ids = request.json["raceIds"]
    year = request.json["year"]

    # delete all toggle info for this user and season which handles both duplicates and untoggles
    season_races = Race.query.filter(Race.season_year == year).all()

    season_ids = [race.id for race in season_races]

    season_user_changes = User_Change.query.filter(User_Change.race_id.in_(season_ids), User_Change.user_id == g.user.id).delete()
    db.session.commit()

    # add new User Changes
    if len(race_ids):
        for id in race_ids:
            new_user_change = User_Change(
                race_id=id,
                user_id=g.user.id
            )
            db.session.add(new_user_change)

        db.session.commit()

    return json.jsonify("Changes Saved!")
