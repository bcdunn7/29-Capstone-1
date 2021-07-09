from app import app
from models import db, Season, Driver, Race, Finish, Selected_Driver
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

    # Drivers
    
    # Get list of all drivers currently to see if they already exist in DB
    all_drivers = Driver.query.all()
    already_driver = [d.code for d in all_drivers]
    
    for res in races[0]['Results']:
        if res['Driver']['code'] in drivers and res['Driver']['code'] not in already_driver:
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

    # after both season and drives are added:
    # add selected_drivers:
    driver_ids = db.session.query(Driver.id).filter(Driver.code.in_(drivers)).all()

    for d_id in driver_ids:
        sd = Selected_Driver(
            season_year = year,
            driver_id = d_id[0]
        )
        db.session.add(sd)

    # Commit all
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

# s2007
bahrain_2007 = Race.query.filter(Race.season_year == 2007, Race.abbreviation == 'BHR').first()
bahrain_2007.blurb = "Bahrain: After Bahrain, Alonso, Räikkönen and Hamilton were equal on points. The last time the top three were level on points was in 1950 after the Indianapolis 500. By finishing second, Hamilton became the first driver in Formula One history to finish on the podium in each of his first three Formula 1 Grands Prix; the previous record was two consecutive podium finishes, achieved by Peter Arundell in the 1964 season."
db.session.add(bahrain_2007)

spain_2007 = Race.query.filter(Race.season_year == 2007, Race.abbreviation == 'ESP').first()
spain_2007.blurb = "Spain: Massa won this race by almost seven seconds over the McLaren pair of Hamilton and Alonso, respectively second and third. This result meant that Hamilton, after a Formula One career of only four races, led the championship. He is the youngest driver to do so, taking the record from McLaren team founder, Bruce McLaren."
db.session.add(spain_2007)

monaco_2007 = Race.query.filter(Race.season_year == 2007, Race.abbreviation == 'MON').first()
monaco_2007.blurb = "Monaco: Around the tight streets of Monaco, Kimi Räikkönen found himself in the barriers just pas the Swimming Pool Complex in the second qualifying stage, breaking his front-right suspension. The damage inflicted could not be repaired and he qualified sixteenth. Despite this horrendous qualifying performance, Räikkönen raced through the field to finish 8th gaining himself one championship point, the exact margin he ended up winning the Championship by."
db.session.add(monaco_2007)

canada_2007 = Race.query.filter(Race.season_year == 2007, Race.abbreviation == 'CAN').first()
canada_2007.blurb = "Canada: An early crash on lap 22 led to a pit-stop-brigade, but Felipe Massa accidentally left the pit lane while the red exit light was on, disqualifying him from the race. Although it's unclear where he would have finished, it's likely he could have picked up around 8 points if he had not been disqualified. Just a few laps from the finish line, Alonso was also overtaken by Takuma Sato around the final chicane scoring him only 2 points in 7th place instead of 3 points in 6th."
db.session.add(canada_2007)

france_2007 = Race.query.filter(Race.season_year == 2007, Race.abbreviation == 'FRA').first()
france_2007.blurb = "France: In a race that favored the top teams (Massa, Hamilton, Räikkönen were the top three), Alonso was unable to complete a single lap in the final qualifying session (Q3) due to a gearbox issue. He only finished 7th with 2 points. Even a fourth place, which would have been easily achievable without his gearbox failure, would have scored him an additional 3 points and the title by the end of the year."
db.session.add(france_2007)

turkey_2007 = Race.query.filter(Race.season_year == 2007, Race.abbreviation == 'TUR').first()
turkey_2007.blurb = "Turkey: Hamilton found himself in the middle of the race quickly chasing down Räikkönen in second, but a surprise puncture forced him to drop to 5th only scoring 4 points instead of the likely 8 points he would have scored after passing Räikkönen."
db.session.add(turkey_2007)

italy_2007 = Race.query.filter(Race.season_year == 2007, Race.abbreviation == 'ITA').first()
italy_2007.blurb = "Italy: Massa who has started well in 3rd, retired from the race after a suspension failure. This left Massa fourth in the title fight and behind the leader by 23 points, a margin he would never make up."
db.session.add(italy_2007)

japan_2007 = Race.query.filter(Race.season_year == 2007, Race.abbreviation == 'JPN').first()
japan_2007.blurb = "Italy: Massa who has started well in 3rd, retired from the race after a suspension failure. This left Massa fourth in the title fight and behind the leader by 23 points, a margin he would never make up."
db.session.add(japan_2007)

china_2007 = Race.query.filter(Race.season_year == 2007, Race.abbreviation == 'CHN').first()
china_2007.blurb = "China: Hamilton was now 12 points in the lead for the Drivers' Championship with only 2 races to complete. He was leading this race before struggling with tire ware in the wet conditions and needing to pit. On his way into the pit entry, however, Hamilton failed to surmount the sharp left-hander and beached his car in the gravel where he was unable to get his car going and suffered the first retirement of his F1 career, ultimately costing him the Drivers' Championship in his rookie season."
db.session.add(china_2007)

brazil_2007 = Race.query.filter(Race.season_year == 2007, Race.abbreviation == 'BRA').first()
brazil_2007.blurb = "Brazil: Coming into the final race of the season, Hamilton was still leading the title fight with 107 points followed by Alonso (103) and Räikkönen (100). Lewis Hamilton also started the race ahead of title contenders Räikkönen and Alonso. But just a few laps into the race Hamilton suffered a gearbox issue and stalled the car for close to 30 seconds. By the time the Briton restarted his car, he was in 18th. He raced an arduous recovery drive finishing 7th and scoring 2 points. But Räikkönen who had capitalized by the current race leader Massa, won the race, scoring 10 points edging out both Hamilton and Alonso (109 points each) by 1 point, and winning the Drivers' Championship with 110 points. Hamilton lost the title in the final race of his rookie season after leading it since race 6. Räikkönen won the title after not leading the championship since the very first race of the season."
db.session.add(brazil_2007)


# s2010

# **********************
#Commit all
db.session.commit()