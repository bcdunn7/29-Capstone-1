"""User and main app view tests."""

import os
from unittest import TestCase

from models import db, User, Season, Race, User_Change

os.environ['DATABASE_URL'] = "postgresql:///influence-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class MainViewsTestCase(TestCase):
    """Test views for main."""

    def setUp(self):
        """Create test client, add sample user."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

    
    def tearDown(self):
        """Teardown."""

        db.session.rollback()


    def test_show_homepage(self):
        """Show homepage?"""

        with self.client as c:
            resp = c.get('/')

            self.assertEqual(resp.status_code, 200)

            self.assertIn('<div class="h5">InfluenceF1</div>', str(resp.data))

    
    def test_show_tutorial(self):
        """Show tutorial?"""

        with self.client as c:
            resp = c.get('/how-it-works')

            self.assertEqual(resp.status_code, 200)

            self.assertIn('<h2>How it works:</h2>', str(resp.data))


class UserViewsTestCase(TestCase):
    """Test views for user."""

    def setUp(self):
        """Create test client, add sample user."""

        db.drop_all()
        db.create_all()

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

    
    def test_show_login(self):
        """Show login page?"""

        with self.client as c:
            resp = c.get('/login')

            self.assertEqual(resp.status_code, 200)

            self.assertIn('<div class="h2">Log in</div>', str(resp.data))


    def test_show_login_already_logged_in(self):
        """No view if already logged in?"""

        with self.client as c:
            with c.session_transaction() as session:
                session[CURR_USER_KEY] = self.testuser1.id

            resp = c.get('/login', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

            self.assertIn('<div class="h5">InfluenceF1</div>', str(resp.data))


    def test_show_signup(self):
        """Show signup page?"""

        with self.client as c:
            resp = c.get('/signup')

            self.assertEqual(resp.status_code, 200)

            self.assertIn('<div class="h2">Sign up</div>', str(resp.data))


    def test_show_signup_already_logged_in(self):
        """No view if already logged in?"""

        with self.client as c:
            with c.session_transaction() as session:
                session[CURR_USER_KEY] = self.testuser1.id

            resp = c.get('/signup', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

            self.assertIn('<div class="h5">InfluenceF1</div>', str(resp.data))


    def test_logout(self):
        """logout?"""

        with self.client as c:
            with c.session_transaction() as session:
                session[CURR_USER_KEY] = self.testuser1.id

            resp = c.post('/logout', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

            self.assertIn("Successfully logged out", str(resp.data))


    def test_show_profile(self):
        """Show profile?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser1.id
            
            resp = c.get('/profile')

            self.assertEqual(resp.status_code, 200)

            self.assertIn('<div class="h3">User:', str(resp.data))


    def test_profile_view_no_user(self):
        """Redirect to login if no user on show profile?"""

        with self.client as c:
            resp = c.get('/profile', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

            self.assertIn('<div class="h2">Log in</div>', str(resp.data))


    def test_delete_user_data(self):
        """Delete data?"""

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

        db.session.add(r)
        db.session.commit()

        race = Race.query.first()
        user = User.query.first()

        uc = User_Change(
            race_id=race.id,
            user_id=user.id)

        db.session.add(uc)
        db.session.commit()

        self.assertIsNotNone(User_Change.query.first())

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser1.id

            resp = c.post('/erase', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

            self.assertIn('Data Deleted', str(resp.data))

            self.assertIsNone(User_Change.query.first())



    def test_delete_user(self):
        """Delete user?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser1.id

            resp = c.post('/profile', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

            self.assertIn('User Successfully Deleted', str(resp.data))

            self.assertIsNone(User.query.get(1))
