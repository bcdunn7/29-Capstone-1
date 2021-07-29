"""Simulator view tests."""

import os
from unittest import TestCase

from models import db, User, User_Change

os.environ['DATABASE_URL'] = "postgresql:///influence-test"

from app import app, CURR_USER_KEY

import seed

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class SimulatorViewsTestCase(TestCase):
    """Test views for simulator."""

    def setUp(self):
        """Create test client, add sample user."""

        User.query.delete()

        self.client = app.test_client()

        self.testuser1 = User.signup(
            username="testuser1",
            password="password"
        )

        self.testuser1.id = 1

        db.session.commit()


    def tearDown(self):
        """Teardown."""

        db.session.rollback()


    def test_simulator_view_2007(self):
        """Show 2007 simulator page?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser1.id

        resp = c.get('/simulator/2007')

        self.assertEqual(resp.status_code, 200)

        self.assertIn('<canvas id="chartjs-simulator"', str(resp.data))
        
        self.assertIn('2007', str(resp.data))


    def test_simulator_view_2010(self):
        """Show 2010 simulator page?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser1.id

        resp = c.get('/simulator/2010')

        self.assertEqual(resp.status_code, 200)

        self.assertIn('<canvas id="chartjs-simulator"', str(resp.data))
        
        self.assertIn('2010', str(resp.data))


    def test_simulator_view_no_user(self):
        """Redirect to login if no user?"""

        with self.client as c:
            resp = c.get('/simulator/2007', follow_redirects=True)
        
            self.assertEqual(resp.status_code, 200)

            self.assertIn('<div class="h2">Log in</div>', str(resp.data))


    def test_save_toggle_arrangement(self):
        """Save toggle arrangement?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser1.id

            resp = c.post('/simulator/save', json={
                'raceIds': [5],
                'year': 2007})

            self.assertIn('Changes Saved', str(resp.data))

            uc = User_Change.query.first()

            self.assertEqual(uc.race_id, 5)

            self.assertEqual(uc.user_id, 1)
