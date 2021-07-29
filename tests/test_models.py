"""Model tests."""

import os
from unittest import TestCase
from models import db, User, Season, Race, Driver, Finish, Selected_Driver, Change, User_Change
from sqlalchemy import exc

os.environ['DATABASE_URL'] = "postgresql:///influence-test"

from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """Test User model."""

    def setUp(self):
        """Create test client."""

        User.query.delete()

        user1 = User.signup(
            username="testuser",
            password="password"
        )

        db.session.add(user1)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_signup_user_model(self):
        """Does basic model work?"""

        u = User.signup(
            username="testing",
            password="password123"
        )

        db.session.add(u)
        db.session.commit()

        user = User.query.filter_by(username="testing").first()

        self.assertTrue(user)
        self.assertEqual(u, user)
        self.assertTrue(user.password.startswith('$2b$'))


    def test_invalid_user_signup(self):
        """Error if invalid user?"""

        user = User.signup(
            username="testuser", #already taken
            password="somepasswordhere"
        )

        self.assertRaises(exc.InvalidRequestError)

    
    def test_invalid_signup_no_password(self):
        """Error if no password on signup?"""

        with self.assertRaises(ValueError):
            user = User.signup(
                username="testinguser",
                password=""
            )


    def test_authenticate(self):
        """Authenticates?"""

        user = User.authenticate(username="testuser", password="password")

        self.assertTrue(user)


    def test_authenticate_incorrect_username(self):
        """Fail auth if incorrect username?"""

        user = User.authenticate(username="INVALID", password="password")

        self.assertFalse(user)


    def test_authenticate_incorrect_password(self):
        """Fail auth if incorrect pasword?"""

        user = User.authenticate(username="testuser",password="INVALID")

        self.assertFalse(user)


# Most other models are static and not manipulatable by the user so testing the models themselves is less involved

class SeasonModelsTestCase(TestCase):
    """Test Season Model."""

    def setUp(self):
        """Set up for season tests."""

        Season.query.delete()

    
    def tearDown(self):
        """Teardown."""

        db.session.rollback()


    def test_season_model(self):
        """Does basic season model work?"""

        s = Season(
            year=2017,
            rounds=20,
            headline="Some headline.",
            overview="OverviewOverviewOverviewOverviewOverviewOverviewOverviewOverview"
        )

        db.session.add(s)
        db.session.commit()

        season = Season.query.get(2017)

        self.assertTrue(season)
        self.assertEqual(season.rounds, 20)
        self.assertEqual(season.headline, 'Some headline.')
        self.assertEqual(season.overview, 'OverviewOverviewOverviewOverviewOverviewOverviewOverviewOverview')


    def test_create_season_without_nullable_fields(self):
        """Create season without nullable fields?"""

        s = Season(
            year=2017,
            rounds=20
        )

        db.session.add(s)
        db.session.commit()

        season = Season.query.get(2017)

        self.assertTrue(season)

    
    def test_fail_season_creation(self):
        """Fail creation if missing non-nullable?"""

        with self.assertRaises(exc.IntegrityError):
            s = Season(
                year=2017
            )

            db.session.add(s)
            db.session.commit()


class RaceModelsTestCase(TestCase):
    """Test race Model."""

    def setUp(self):
        """Set up for race tests."""

        Race.query.delete()
        Season.query.delete()

        s = Season(year=2017, rounds=20)
        db.session.add(s)
        db.session.commit()


    def tearDown(self):
        """Teardown"""

        db.session.rollback()


    def test_race_model(self):
        """Does basic race model work?"""

        r = Race(
            season_year=2017,
            round=2,
            name="Some Name.",
            abbreviation="ABR",
            blurb="blurb",
            change_text="change text here"
        )

        db.session.add(r)
        db.session.commit()

        race = Race.query.filter_by(season_year=2017).first()

        self.assertTrue(race)
        self.assertEqual(race.round, 2)
        self.assertEqual(race.name, 'Some Name.')
        self.assertEqual(race.blurb, 'blurb')
        self.assertEqual(race.change_text, 'change text here')


    def test_create_race_without_nullable_fields(self):
        """Create race without nullable fields?"""

        r = Race(
            season_year=2017,
            round=2,
            name="Some Name.",
            abbreviation="ABR"
        )

        db.session.add(r)
        db.session.commit()

        race = Race.query.filter_by(season_year=2017).first()

        self.assertTrue(race)
        self.assertEqual(race.round, 2)
        self.assertEqual(race.name, 'Some Name.')

    
    def test_fail_race_creation(self):
        """Fail creation if missing non-nullable?"""

        with self.assertRaises(exc.IntegrityError):
            r = Race(
                season_year=2017,
                # missing round
                name="Some Name.",
                abbreviation="ABR"
            )

            db.session.add(r)
            db.session.commit()


class DriverModelsTestCase(TestCase):
    """Test driver Model."""

    def setUp(self):
        """Set up for driver tests."""

        Driver.query.delete()


    def tearDown(self):
        """Teardown"""

        db.session.rollback()


    def test_driver_model(self):
        """Does basic driver model work?"""

        d = Driver(
            first_name="first",
            last_name='last',
            code='COD'
        )

        db.session.add(d)
        db.session.commit()

        driver = Driver.query.filter_by(code='COD').first()

        self.assertTrue(driver)
        self.assertEqual(driver.first_name, 'first')
        self.assertEqual(driver.last_name, 'last')
        self.assertEqual(driver.code, 'COD')

    
    def test_fail_driver_creation(self):
        """Fail creation if missing non-nullable?"""

        with self.assertRaises(exc.IntegrityError):
            d = Driver(
            first_name="first",
            # missing last name
            code='COD'
            )

            db.session.add(d)
            db.session.commit()


class FinishModelsTestCase(TestCase):
    """Test finish Model."""

    def setUp(self):
        """Set up for finish tests."""

        Finish.query.delete()
        Race.query.delete()
        Driver.query.delete()
        Season.query.delete()

        s = Season(year=2017, rounds=20)
        db.session.add(s)
        db.session.commit()

        r = Race(
            season_year=2017,
            round=2,
            name="Some Name.",
            abbreviation="ABR",
            blurb="blurb",
            change_text="change text here"
        )


        d = Driver(
            first_name="first",
            last_name='last',
            code='COD'
        )

        db.session.add(d)
        db.session.add(r)
        db.session.commit()


    def tearDown(self):
        """Teardown"""

        db.session.rollback()


    def test_finish_model(self):
        """Does basic finish model work?"""

        race = Race.query.first()
        driver = Driver.query.first()
        
        f = Finish(
            race_id=race.id,
            driver_id=driver.id,
            position=5,
            points=10
        )

        db.session.add(f)
        db.session.commit()

        finish = Finish.query.filter_by(race_id=race.id).first()

        self.assertTrue(finish)
        self.assertEqual(finish.race, race)
        self.assertEqual(finish.driver, driver)
        self.assertEqual(finish.position, 5)

    
    def test_fail_finish_creation(self):
        """Fail creation if missing non-nullable?"""

        with self.assertRaises(exc.IntegrityError):
            f = Finish(
            # missing race_id, driver_id,
            position=5,
            points=10
            )

            db.session.add(f)
            db.session.commit()

    
    def test_fail_finish_creation_if_invalid_relationships(self):
        """Fail creation if invalid race id?"""

        Race.query.delete()

        driver = Driver.query.first()


        with self.assertRaises(exc.IntegrityError):
            f = Finish(
            race_id=9999, # not a valid race id
            driver_id=driver.id,
            position=5,
            points=10
            )

            db.session.add(f)
            db.session.commit()

    
class Selected_DriverModelsTestCase(TestCase):
    """Test selected_driver Model."""

    def setUp(self):
        """Set up for selected_driver tests."""

        Driver.query.delete()
        Season.query.delete()
        Selected_Driver.query.delete()

        s = Season(year=2017, rounds=20)
        db.session.add(s)
        db.session.commit()

        d = Driver(
            first_name="first",
            last_name='last',
            code='COD'
        )

        db.session.add(d)
        db.session.commit()


    def tearDown(self):
        """Teardown"""

        db.session.rollback()


    def test_selected_driver_model(self):
        """Does basic selected_driver model work?"""

        season = Season.query.first()
        driver = Driver.query.first()
        
        sd = Selected_Driver(
            season_year=season.year,
            driver_id=driver.id
        )

        db.session.add(sd)
        db.session.commit()

        selected = Selected_Driver.query.first()

        self.assertTrue(selected)

    
    def test_fail_selected_driver_creation(self):
        """Fail creation if missing non-nullable?"""

        driver = Driver.query.first()

        with self.assertRaises(exc.IntegrityError):
            sd = Selected_Driver(
            # missing season_id
            driver_id=driver.id
            )

            db.session.add(sd)
            db.session.commit()

    
    def test_fail_selected_driver_creation_if_invalid_relationships(self):
        """Fail creation if invalid season id?"""

        Season.query.delete()

        driver = Driver.query.first()


        with self.assertRaises(exc.IntegrityError):
            sd = Selected_Driver(
            season_year=9999, # not a valid season id
            driver_id=driver.id
            )

            db.session.add(sd)
            db.session.commit()


class ChangeModelsTestCase(TestCase):
    """Test change Model."""

    def setUp(self):
        """Set up for Change tests."""

        Driver.query.delete()
        Season.query.delete()
        Race.query.delete()
        Change.query.delete()

        s = Season(year=2017, rounds=20)
        db.session.add(s)
        db.session.commit()

        r = Race(
            season_year=2017,
            round=2,
            name="Some Name.",
            abbreviation="ABR",
            blurb="blurb",
            change_text="change text here"
        )

        d = Driver(
            first_name="first",
            last_name='last',
            code='COD'
        )

        db.session.add(d)
        db.session.add(r)
        db.session.commit()


    def tearDown(self):
        """Teardown"""

        db.session.rollback()


    def test_change_model(self):
        """Does basic Change model work?"""

        season = Season.query.first()
        race = Race.query.first()
        driver = Driver.query.first()
        
        c = Change(
            season_year=season.year,
            race_id=race.id,
            driver_id=driver.id,
            new_position=5,
            new_points=10
        )

        db.session.add(c)
        db.session.commit()

        change = Change.query.first()

        self.assertTrue(change)
        self.assertEqual(change.season, season)
        self.assertEqual(change.race, race)
        self.assertEqual(change.driver, driver)

    
    def test_fail_change_creation(self):
        """Fail creation if missing non-nullable?"""

        driver = Driver.query.first()
        season = Season.query.first()
        race = Race.query.first()

        with self.assertRaises(exc.IntegrityError):
            c = Change(
                season_year=season.year,
                race_id=race.id,
                driver_id=driver.id,
                # missing position and points
            )

            db.session.add(c)
            db.session.commit()

    
    def test_fail_change_creation_if_invalid_relationships(self):
        """Fail creation if invalid season id?"""

        season = Season.query.first()
        race = Race.query.first()

        with self.assertRaises(exc.IntegrityError):
            
            c = Change(
                season_year=season.year,
                race_id=race.id,
                driver_id=999, # invalid
                new_position=5,
                new_points=10
            )

            db.session.add(c)
            db.session.commit()


class User_ChangeModelsTestCase(TestCase):
    """Test for User_Change model."""

    def setUp(self):
        """Set up for user_change tests"""

        Season.query.delete()
        Race.query.delete()
        User.query.delete()

        s = Season(year=2017, rounds=20)
        db.session.add(s)
        db.session.commit()

        r = Race(
            season_year=2017,
            round=2,
            name="Some Name.",
            abbreviation="ABR",
            blurb="blurb",
            change_text="change text here"
        )

        user1 = User.signup(
            username="testuser",
            password="password"
        )

        db.session.add(r)
        db.session.add(user1)
        db.session.commit()
        

    def tearDown(self):
        """Teardown."""

        db.session.rollback()

    
    def test_user_change_model(self):
        """Does basic model work?"""

        race = Race.query.first()
        user = User.query.first()

        uc = User_Change(
            race_id=race.id,
            user_id=user.id
        )

        db.session.add(uc)
        db.session.commit()

        userChange = User_Change.query.first()

        self.assertTrue(userChange)
        self.assertEqual(userChange.race, race)
        self.assertEqual(userChange.user, user)

    
    def test_fail_user_change_creation(self):
        """Fail user change creation if invalid id?"""

        with self.assertRaises(exc.IntegrityError):
            user = User.query.first()

            uc = User_Change(
                race_id=9999, # invalid
                user_id=user.id
            )

            db.session.add(uc)
            db.session.commit()
