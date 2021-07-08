from app import app
from models import db, Season, Driver, Race, Finish
from abbreviations import race_abbrs
import requests

API_BASE_URL = "https://ergast.com/api/f1"

#Drop and Create all Tables

db.drop_all()
db.create_all()

# **********************************
# Season API Call and Data Insertion
def make_API_call_and_generate_data(year, drivers):
    """Makes a call to the eargast API for a given season(year) and generates all baseline database data"""

    #Need to find how long data is, which is returned from the API

    limit_resp = requests.get(f"{API_BASE_URL}/{year}/results.json?limit=1")

    limit_json = limit_resp.json()

    limit = limit_json['MRData']['total']

    #Now we can make the full API Request with all data returned
    resp = requests.get(f"{API_BASE_URL}/{year}/results.json?limit={limit}")

    r_json = resp.json()

    data = r_json['MRData']['RaceTable']

    races = data['Races']

    #Season
    s = Season(
        year = int(data['season']),
        rounds = len(races)
    )
    db.session.add(s)

    #Drivers
    for res in races[0]['Results']:
        if res['Driver']['code'] in drivers:
            driv_data = res['Driver']
            d = Driver(
                first_name = driv_data['givenName'],
                last_name = driv_data['familyName'],
                code = driv_data['code'])
            db.session.add(d)

    #commit for season and drivers, as those are needed for races and finishes below
    db.session.commit()

    #find season
    season = Season.query.filter_by(year=int(data['season'])).first()

    #get race abbreviations for this season

    season_race_abbrs = race_abbrs[f"race_abbrs_{data['season']}"]

    #Races
    for race in races:
        race_name = race['raceName']
        r = Race(
            season_year = season.year,
            round = race['round'],
            name = race_name,
            abbreviation = season_race_abbrs[f'{race_name}']
        )
        db.session.add(r)

    #Finishes
    for race in races:
        #get db info obj

        r = Race.query.filter(Race.season_year == (season.year), Race.round == int(race['round'])).first()
        
        # loop through results to create finishes
        results = race['Results']
        for result in results:
            if result['Driver']['code'] in drivers:
                #get driver db info obj
                d = Driver.query.filter_by(code=result['Driver']['code']).first()
                #find finish position and points (what a given driver scored in a given race)
                position = int(result['position'])
                points = int(result['points'])

                #create finish instance
                f = Finish(
                    race_id = r.id,
                    driver_id = d.id,
                    position = position,
                    points = points
                )
                db.session.add(f)

    #Commit all
    db.session.commit()


# ********************
# Calls for Specific Seasons:
# Must pass in specific year and array of drivers to select

make_API_call_and_generate_data(2007, ['RAI', 'HAM', "ALO", "MAS"])

make_API_call_and_generate_data(2010, ['VET', 'ALO', 'WEB', 'HAM', 'BUT', 'MAS'])

# This function currently uses driver codes for disambiguation, but the API does not support codes for all (namely, older) seasons. A modified function would need to be created for those

#********************
# Add non-API data
# like headline for season, blurbs



# **********************
#Commit all
db.session.commit()