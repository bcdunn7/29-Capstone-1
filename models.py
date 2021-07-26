"""Models for influenceF1 app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import backref

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect database to Flask app."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User model."""

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                primary_key=True,
                autoincrement=True)

    username = db.Column(db.String(128),
                unique=True,
                nullable=False)

    password = db.Column(db.Text,
                nullable=False)

    user_changes = db.relationship('User_Change', 
                back_populates='user', cascade="all, delete-orphan")

    @classmethod
    def signup(cls, username, password):
        """Sign up user. With Bcrypt for password hashing."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(username=username, password=hashed_pwd)

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Authenticate user on login. Returns user if valid, returns false if no user found or invalid password."""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_authenticated = bcrypt.check_password_hash(user.password, password)
            if is_authenticated:
                return user

        return False


class Season(db.Model):
    """Season model."""

    __tablename__ = 'seasons'

    year = db.Column(db.Integer,
                primary_key=True)

    rounds = db.Column(db.Integer,
                nullable=False)

    headline = db.Column(db.Text)

    overview = db.Column(db.Text)

    races = db.relationship('Race',
                back_populates='season', cascade="all, delete-orphan")

    drivers = db.relationship('Driver',
                secondary='selected_drivers',
                backref='seasons')


class Race(db.Model):
    """Race model."""

    __tablename__ = 'races'

    id = db.Column(db.Integer,
                primary_key=True,
                autoincrement=True)

    season_year = db.Column(db.Integer,
                db.ForeignKey('seasons.year', 
                ondelete='CASCADE'),
                nullable=False)

    round = db.Column(db.Integer,
                nullable=False)

    name = db.Column(db.Text,
                nullable=False)

    abbreviation = db.Column(db.Text,
                default="N/A")

    blurb = db.Column(db.Text)

    change_text = db.Column(db.Text)

    season = db.relationship('Season')

    finishes = db.relationship('Finish', 
                back_populates='race', cascade="all, delete-orphan")


class Driver(db.Model):
    """Driver model."""

    __tablename__ = 'drivers'

    id = db.Column(db.Integer,
                primary_key=True,
                autoincrement=True)

    first_name = db.Column(db.Text,
                nullable=False) 

    last_name = db.Column(db.Text,
                nullable=False)

    code = db.Column(db.Text,
                nullable=False)

    finishes = db.relationship('Finish',
                back_populates='driver', cascade="all, delete-orphan")


class Finish(db.Model):
    """Finish model."""

    __tablename__ = 'finishes'

    id = db.Column(db.Integer,
                primary_key=True,
                autoincrement=True)

    race_id = db.Column(db.Integer,
                db.ForeignKey('races.id', 
                ondelete='CASCADE'),
                nullable=False)

    driver_id = db.Column(db.Integer,
                db.ForeignKey('drivers.id', 
                ondelete='CASCADE'),
                nullable=False)

    position = db.Column(db.Integer,
                nullable=False)

    points = db.Column(db.Float,
                nullable=False)

    driver = db.relationship('Driver')

    race = db.relationship('Race')


class Selected_Driver(db.Model):
    """Selected_Driver model for drivers to be studied within each season."""

    __tablename__ = 'selected_drivers'

    id = db.Column(db.Integer,
                primary_key=True,
                autoincrement=True)

    season_year = db.Column(db.Integer,
                db.ForeignKey('seasons.year', 
                ondelete='CASCADE'),
                nullable=False)

    driver_id = db.Column(db.Integer,
                db.ForeignKey('drivers.id', 
                ondelete='CASCADE'),
                nullable=False)


class Change(db.Model):
    """Chande model for manipulatable data points."""

    __tablename__ = 'changes'

    id = db.Column(db.Integer,
                primary_key=True,
                autoincrement=True)

    season_year = db.Column(db.Integer,
                db.ForeignKey('seasons.year', 
                ondelete='CASCADE'),
                nullable=False)

    race_id = db.Column(db.Integer,
                db.ForeignKey('races.id',
                ondelete='CASCADE'),
                nullable=False)

    driver_id = db.Column(db.Integer,
                db.ForeignKey('drivers.id', 
                ondelete='CASCADE'),
                nullable=False)

    new_position = db.Column(db.Integer,
                nullable=False)

    new_points = db.Column(db.Float,
                nullable=False)

    season = db.relationship('Season')

    race = db.relationship('Race')

    driver = db.relationship('Driver')


class User_Change(db.Model):
    """User_Change model for user manipulated values. Race_id is used since it functions as a grouping mechanism for the different changes."""

    __tablename__ = 'user_changes'

    race_id = db.Column(db.Integer,
                db.ForeignKey('races.id', 
                ondelete='CASCADE'),
                primary_key=True)

    user_id = db.Column(db.Integer,
                db.ForeignKey('users.id',
                ondelete='CASCADE'),
                primary_key=True)

    race = db.relationship('Race')

    user = db.relationship('User')