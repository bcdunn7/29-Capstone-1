"""Helpers tests."""

import os
from unittest import TestCase
from models import db, User, Season, Race, Driver, Finish, Selected_Driver, Change, User_Change
from sqlalchemy import exc

os.environ['DATABASE_URL'] = "postgresql:///influence-test"

from app import CURR_USER_KEY, app, add_user_to_g

from flask import g

import seed

from helpers import get_data_for_simulator, get_changes_data, get_user_changes, get_blurbs_for_races

db.create_all()

class HelpersTestCase(TestCase):
    """Test helpers functions."""

    def setUp(self):
        """Create test client."""

        User.query.delete()

        self.client = app.test_client()

        self.testuser1 = User.signup(
            username="testuser1",
            password="password"
        )

        self.testuser1.id = 1

        db.session.commit()


    def tearDown(self):
        db.session.rollback()


    def test_get_data_for_simulator(self):
        """Test get_data_for_simulator."""

        result = get_data_for_simulator(2007)

        self.assertEqual(len(result), 2)

        self.assertEqual(len(result[0]), 18)

        self.assertEqual(len(result[1]), 4)
        
        self.assertIn("'label': 'HAM'", str(result[1]))

        self.assertEqual(len(result[1][0]['data']), 18)


    def test_get_changes_data(self):
        """Test get_changes_data."""

        result = get_changes_data(2007)

        self.assertEqual(len(result), 2)

        self.assertEqual(len(result[0]), 8)

        self.assertEqual(len(result[1]), 20)

        self.assertIn("'driver': 'RAI'", str(result[1]))

        self.assertIn("change_text", str(result[0]))


    def test_get_user_changes(self):
        """Test get_user_changes."""

        uc1 = User_Change(
            race_id=1, 
            user_id=self.testuser1.id)
        uc2 = User_Change(
            race_id=2, 
            user_id=self.testuser1.id)

        db.session.add(uc1)
        db.session.add(uc2)
        db.session.commit()

        with app.app_context():
            with self.client as c:
                with c.session_transaction() as sess:
                    sess[CURR_USER_KEY] = self.testuser1.id

                if CURR_USER_KEY in sess: 
                    g.user = User.query.get(sess[CURR_USER_KEY])

            result = get_user_changes(2007)

            self.assertEqual(len(result), 2)

            self.assertEqual([1,2], result)


    def test_get_blurbs_for_races(self):
        """Test get race blurbs."""

        result = get_blurbs_for_races(2007)

        self.assertEqual(len(result), 10)

        self.assertIn("Peter Arundell in the 1964 season", str(result))
