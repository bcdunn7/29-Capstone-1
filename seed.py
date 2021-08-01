from app import app
from models import db, Season, Driver, Race, Finish, Selected_Driver, Change
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

make_API_call_and_generate_data(2008, ['HAM', 'MAS' 'KUB', 'RAI'])

# This function currently uses driver codes for disambiguation, but the API does not support codes for all (namely, older than 2005) seasons. A modified function would need to be created for those

#********************
# Add non-API data
# like headline and overview for season, race blurbs

# s2007
s2007 = Season.query.get(2007)
s2007.overview = "The 2007 F1 season saw the temporary retirement of F1 great Michael Schumacher, leaving Ferrari with an open seat. This seat was filled by the Finnish driver Kimi Räikkönen leaving his previous team McLaren with an open seat as well. This seat was taken by the 2005 and 2006 World Champion Fernando Alonso, leaving Renault after 5 years. The ever-great Ferrari of Räikkönen versus McLaren with their powerful MP4-22 chassis and the defending world Champion looked like the looming title fight, but it was not only Alonso who would prove to be successful in a McLaren. Alonso's teammate, rookie Lewis Hamilton would have a historic rookie season in F1 adding a third name to the title fight. Although ultimately falling away, Räikkönen's teammate Felipe Massa added a fourth challenger in the Drivers' Championship battel early on. With both veteran greats and rookie all-stars, the 2007 was one of the most intriguing and close fought drivers' titles in F1 history."
s2007.headline = "Räikkönen 110 — Hamilton 109 — Alonso 109 — Massa 94"
db.session.add(s2007)

bahrain_2007 = Race.query.filter(Race.season_year == 2007, Race.abbreviation == 'BHR').first()
bahrain_2007.blurb = "Bahrain: After the Bahrain Grand Prix, Alonso, Räikkönen and Hamilton were equal on points. The last time the top three were level on points was in 1950 after the Indianapolis 500. By finishing second, Hamilton became the first driver in Formula One history to finish on the podium in each of his first three Formula 1 Grands Prix; the previous record was two consecutive podium finishes, achieved by Peter Arundell in the 1964 season."
db.session.add(bahrain_2007)

spain_2007 = Race.query.filter(Race.season_year == 2007, Race.abbreviation == 'ESP').first()
spain_2007.blurb = "Spain: Massa won this race by almost seven seconds over the McLaren pair of Hamilton and Alonso, respectively second and third. This result meant that Hamilton, after a Formula One career of only four races, led the championship. He is the youngest driver to do so, taking the record from McLaren team founder, Bruce McLaren."
db.session.add(spain_2007)

monaco_2007 = Race.query.filter(Race.season_year == 2007, Race.abbreviation == 'MON').first()
monaco_2007.blurb = "Monaco: Around the tight streets of Monaco, Kimi Räikkönen found himself in the barriers just past the Swimming Pool Complex in the second qualifying stage, breaking his front-right suspension. The damage inflicted could not be repaired and he qualified sixteenth. Despite this horrendous qualifying performance, Räikkönen raced through the field to finish 8th gaining himself one championship point, the exact margin he ended up winning the Championship by."
monaco_2007.change_text = "Räikkönen does not race back to 8th from 16th, instead finishes in 9th (0pts)."
db.session.add(monaco_2007)

canada_2007 = Race.query.filter(Race.season_year == 2007, Race.abbreviation == 'CAN').first()
canada_2007.blurb = "Canada: An early crash on lap 22 led to a pit-stop-brigade, but Felipe Massa accidentally left the pit lane while the red exit light was on, disqualifying him from the race. Although it's unclear where he would have finished, it's likely he could have picked up around 8 points if he had not been disqualified. Just a few laps from the finish line, Alonso was also overtaken by Takuma Sato around the final chicane scoring him only 2 points in 7th place instead of 3 points in 6th."
canada_2007.change_text = "Massa is not DSQ'd and instead finishes 2nd (8pts)."
db.session.add(canada_2007)

france_2007 = Race.query.filter(Race.season_year == 2007, Race.abbreviation == 'FRA').first()
france_2007.blurb = "France: In a race that favored the top teams (Massa, Hamilton, Räikkönen were the top three), Alonso was unable to complete a single lap in the final qualifying session (Q3) due to a gearbox issue. He only finished 7th with 2 points. Even a fourth place, which would have been easily achievable without his gearbox failure, would have scored him an additional 3 points and the title by the end of the year."
france_2007.change_text = "No Q3 mishap for Alonso, instead finishes 4th (5pts)."
db.session.add(france_2007)

turkey_2007 = Race.query.filter(Race.season_year == 2007, Race.abbreviation == 'TUR').first()
turkey_2007.blurb = "Turkey: Hamilton found himself in the middle of the race quickly chasing down Räikkönen in second, but a surprise puncture forced him to drop to 5th only scoring 4 points instead of the likely 8 points he would have scored after passing Räikkönen."
turkey_2007.change_text = "Hamilton doesn't suffer a puncture and finishes 2nd (8pts)."
db.session.add(turkey_2007)

italy_2007 = Race.query.filter(Race.season_year == 2007, Race.abbreviation == 'ITA').first()
italy_2007.blurb = "Italy: Massa who has started well in 3rd, retired from the race after a suspension failure. This left Massa fourth in the title fight and behind the leader by 23 points, a margin he would never make up."
italy_2007.change_text = "Massa avoids suspension issues and finishes 3rd (6pts)."
db.session.add(italy_2007)

japan_2007 = Race.query.filter(Race.season_year == 2007, Race.abbreviation == 'JPN').first()
japan_2007.blurb = "Japan: Alonso, who had begun the race in 2nd, struggled under wet conditions and aquaplaned into the wall on lap 41, forcing him to retire from the race, leaving a likely 8 points on the table."
japan_2007.change_text = "Alonso keeps the car planted in the rain finishing in 2 (8pts)."
db.session.add(japan_2007)

china_2007 = Race.query.filter(Race.season_year == 2007, Race.abbreviation == 'CHN').first()
china_2007.blurb = "China: Hamilton was now 12 points in the lead for the Drivers' Championship with only 2 races to complete. He was leading this race before struggling with tire ware in the wet conditions and needing to pit. On his way into the pit entry, however, Hamilton failed to surmount the sharp left-hander and beached his car in the gravel where he was unable to get his car going and suffered the first retirement of his F1 career, ultimately costing him the Drivers' Championship in his rookie season."
china_2007.change_text = "Hamilton wins the race instead of beaching the car on pit entry (10pts)."
db.session.add(china_2007)

brazil_2007 = Race.query.filter(Race.season_year == 2007, Race.abbreviation == 'BRA').first()
brazil_2007.blurb = "Brazil: Coming into the final race of the season, Hamilton was still leading the title fight with 107 points followed by Alonso (103) and Räikkönen (100). Lewis Hamilton also started the race ahead of title contenders Räikkönen and Alonso. But just a few laps into the race Hamilton suffered a gearbox issue and stalled the car for close to 30 seconds. By the time the Briton restarted his car, he was in 18th. He raced an arduous recovery drive finishing 7th and scoring 2 points. But Räikkönen who had capitalized by the current race leader Massa, won the race, scoring 10 points edging out both Hamilton and Alonso (109 points each) by 1 point, and winning the Drivers' Championship with 110 points. Hamilton lost the title in the final race of his rookie season after leading it since race 6. Räikkönen won the title after not leading the championship since the very first race of the season."
brazil_2007.change_text = "Hamilton suffers no stalling gearbox and istead wins from pole (10pts)."
db.session.add(brazil_2007)


#s2010
s2010 = Season.query.get(2010)
s2010.overview = "Coming off an overly dominant 2009 season where Brawn ran away with the title, 2010 proved to be the exact opposite. The 2010 F1 season was one of the closest and most competitive Driver's Championships in F1 history. Throughout the season there were 6 drivers competing for the title with a record setting 10 changes of leadership in the title race. The title was variously led by every top-6 finisher except for Sebastian Vettel who did not lead the championship until the final race of the season where he finally led the championship and won the title. Vettel's win also set another record making him the youngest Drivers' Champion in F1 history at 23 years 134 years old. With previous F1 champions Michael Schumacher, Fernando Alonso, Jenson Button, Lewis Hamilton, and now Sebastian Vettel, the 2010 season often races to the top of F1 fans' favorite seasons."
s2010.headline = "Vettel 256 — Alonso 252 — Webber 242 — Hamilton 240 — Button 214 — Massa 144"
db.session.add(s2010)

austrailia_2010 = Race.query.filter(Race.season_year == 2010, Race.abbreviation == 'AUS').first()
austrailia_2010.blurb = "Austrailia: After starting on pole and leading the race in the early portions of the Grand Prix, Sebastian Vettel had a mysterious left-front wheel issue resulting in a loss to torque drive between the left front axel and the wheel which prompted a spin into the gravel and a retirement from the race. A win here would have meant after only two races Vettel would have led the championship, a status he did not end up achieving until the final race of the season."
austrailia_2010.change_text = "Vettel suffers no mechanical issues, instead retains lead and wins (25pts)."
db.session.add(austrailia_2010)

malaysia_2010 = Race.query.filter(Race.season_year == 2010, Race.abbreviation == 'MAL').first()
malaysia_2010.blurb = "Malaysia: After a wet qualifying shifted some of the title contenders down in the grid order, the Malaysian Grand Prix was a fairly calm affair until the penultimate lap of the race, when Alonso attempted a move for 8th place but ran wide and surprisingly caused his engine to blow up, retiring him from the race leaving him with 0 points instead of a possible 4."
malaysia_2010.change_text = "Alonso makes the move for 8th stick (4pts)."
db.session.add(malaysia_2010)

spain_2010 = Race.query.filter(Race.season_year == 2010, Race.abbreviation == 'ESP').first()
spain_2010.blurb = "Spain: Racing strong in 2nd on the penultimate lap of the race, Hamilton suffered a puncture and subsequent blowout punting him into the wall. He classified 14th with 0 points leaving what should have been a podium finish and 18 points on the table."
spain_2010.change_text = "No blowout for Hamilton rather a podium finish (18pts)."
db.session.add(spain_2010)

turkey_2010 = Race.query.filter(Race.season_year == 2010, Race.abbreviation == 'TUR').first()
turkey_2010.blurb = "Turkey: The Red Bull pair of Webber and Vettel were leading the race 1-2 before the pair collided on lap 40 forcing Vettel to retire and Webber to drop to 3rd by the end of the race. This accident promoted Hamilton to a race win, with Button in 2nd."
turkey_2010.change_text = "Webber and Vettel do not collide leading home a Red Bull 1-2 (25pts, 18pts)."
db.session.add(turkey_2010)

canada_2010 = Race.query.filter(Race.season_year == 2010, Race.abbreviation == 'CAN').first()
canada_2010.blurb = "Canada: Massa struggled greatly in Canada leaving him in 15th with a dismal 0 points. This was the first in a series of three consecutive races where Massa would finish outside the points, ultimately putting him out of contention for the title for the remainder of the season."
db.session.add(canada_2010)

europe_2010 = Race.query.filter(Race.season_year == 2010, Race.abbreviation == 'EUR').first()
europe_2010.blurb = "Europe: Webber, starting in second, suffered a serious of entanglements with other drivers ultimately culminating in an intense crash with Heikki Kovalainen, sending Webber's car airborne and careening into a tire barrier leaving him with a retirement instead of 18 points."
europe_2010.change_text = "Webber avoids conflilcts with other drivers and retains his second place (18pts)."
db.session.add(europe_2010)

germany_2010 = Race.query.filter(Race.season_year == 2010, Race.abbreviation == 'GER').first()
germany_2010.blurb = "Germany: As the race was nearing its final stages, Ferrari issued team-orders to drivers Massa and Alonso to let Alonso pass Massa for the lead. This extremely controversial move led to an investigation that served Ferrari with a $100,000 fine. But many paddock members and commentators thought both Alonso and Massa should have been stripped of their points as well, leaving them both with 0 points instead of 25 and 18."
germany_2010.change_text = "Alonso and Massa are stripped of their points due to sporting violations (0pts each)."
db.session.add(germany_2010)

hungary_2010 = Race.query.filter(Race.season_year == 2010, Race.abbreviation == 'HUN').first()
hungary_2010.blurb = "Hungary: Hamilton running in fourth suddenly retired with gearbox issues costing him 12 points and the lead of the championship which he had help for the previous four races."
hungary_2010.change_text = "Hamilton avoids gearbox troubles and races home to fourth (12pts)."
db.session.add(hungary_2010)

italy_2010 = Race.query.filter(Race.season_year == 2010, Race.abbreviation == 'ITA').first()
italy_2010.blurb = "Italy: After winning in Belgium, Hamilton once again reclaimed the lead of the championship. But at Monza, Hamilton and Massa came together on the first lap around Curva Grande and into the turn 4 chicane forcing the current leader of the title fight to retire leaving 10 or more points up for grabs."
italy_2010.change_text = "Hamilton and Massa do not tangle and Hamilton picks up 5th (10pts)."
db.session.add(italy_2010)

singapore_2010 = Race.query.filter(Race.season_year == 2010, Race.abbreviation == 'SIN').first()
singapore_2010.blurb = "Singapore: In the middle portion of the race, Hamilton was gaining on Webber and lined up an overtaking maneuver on the Raffles Boulevard straight. However, when the two entered the subsequent corner, Webber's front tire punctured Hamilton's rear tire forcing Hamilton's third retirement in four races and leaving another 15 points on the table."
singapore_2010.change_text = "Webber does not puncture Hamilton's wheel, scoring Hamilton 3rd (15pts)."
db.session.add(singapore_2010)

korea_2010 = Race.query.filter(Race.season_year == 2010, Race.abbreviation == 'KOR').first()
korea_2010.blurb = "Korea: An extremely wet race with poor visibility saw Vettel leading for the majority of the Grand Prix. But on lap 46, a surprise engine failure forced Vettel to retire from the lead losing a possible 25 points. This meant that after the race, Alonso led the Drivers' Championship with 246 points. Red Bull's Webber and Vettel were 2nd and 3rd with 238 and 231 points respectively. Hamilton was not in 4th but was mathematically still in title contention, trailing Alonso by 24 points."
korea_2010.change_text = "Vettel wins from pole, avoiding retirement from engine trouble (25pts)."
db.session.add(korea_2010)

abu_dhabi_2010 = Race.query.filter(Race.season_year == 2010, Race.abbreviation == 'ABU').first()
abu_dhabi_2010.blurb = "Abu Dhabi: Vettel led this race from pole followed by Hamilton and Alonso, with Webber in 5th. However, the Yas Marina Circuit in Abu Dhabi was (and still is) notorious for being difficult to overtake at, so track position is everything. Some early incidents saw Webber and Alonso pit relatively early, rejoining the field in 13th and 14th. Due to the difficult conditions at Yas Marina Alonso and Webber struggled lap after lap to pass Vitaly Petrov and were ultimately unsuccessful finishing in 7th and 8th. Such a poor performance from the two leading title contenders allowed race-winner Sebastian Vettel to win the Drivers' Championship by only 4 points ahead of Alonso."
db.session.add(abu_dhabi_2010)



# 2008

s2008 = Season.query.get(2008)
s2008.overview = "Overview"
s2008.headline = "Hamilton 98 — Massa 97"
db.session.add(s2008)

austrailia_2008 = Race.query.filter(Race.season_year == 2008, Race.abbreviation == 'AUS').first()
austrailia_2008.blurb = "Australia: The first race of the season was an eventful one. Only 7 cars crossed the finish line, and 1 of those was later disqualified. Massa unfortunately collided with David Coulthard on lap 26 forcing him to retire from engine troubles just a few laps later. Hamilton won from pole."
austrailia_2008.change_text = "Massa doesn't collide with Coulthard finishing in 4th (5pts)."
db.session.add(austrailia_2008)

malaysia_2008 = Race.query.filter(Race.season_year == 2008, Race.abbreviation == 'MAL').first()
malaysia_2008.blurb = "Though racing well in the fight for podium, Massa spun off on lap 31 getting his car beached in the gravel. Hamilton managed to pick up 4 points in 5th."
malaysia_2008.change_text = "Massa doesn't spin off and beach his car, finishes 5th (4pts)."
db.session.add(malaysia_2008)

bahrain_2008 = Race.query.filter(Race.season_year == 2008, Race.abbreviation == 'BHR').first()
bahrain_2008.blurb = "Hamilton, who was leading the championship before this race, suffered a poor start, and then later collided with the Renault of Alonso leaving him with an abysmal performance, finishing in 13th."
bahrain_2008.change_text = "Hamtilton has no grid troubles and races away fine in 3rd (6pts)."
db.session.add(bahrain_2008)

canada_2008 = Race.query.filter(Race.season_year == 2008, Race.abbreviation == 'CAN').first()
canada_2008.blurb = "In one of the most dramatic moments of the 2008 season, Hamilton led Räikkönen and Kubica into the pit lane, leading the race. But Räikkönen led the other two out of the pit lane. However, as they approached the exit, Räikkönen had slowed and then quickly come to a stop as the pit lane had a red light at the time. However, Hamilton did not notice the red light and crashed into the back of Räikkönen forcing both drivers to retire."
canada_2008.change_text = "Hamilton avoids dramatic pit lane crash in Canada (6pts)."
db.session.add(canada_2008)

france_2008 = Race.query.filter(Race.season_year == 2008, Race.abbreviation == 'FRA').first()
france_2008.blurb = "Due to a collision with Räikkönen in Canada, Hamilton suffered a 10 place grid penalty, and he could only manage to finish 10th. Massa went on to win the race."
france_2008.change_text = "Hamilton doesn't receive 10 place grid penalty, finishes 3rd (6pts)."
db.session.add(france_2008)

hungary_2008 = Race.query.filter(Race.season_year == 2008, Race.abbreviation == 'HUN').first()
hungary_2008.blurb = "On lap 68 of 70 Massa appeared to be in command of the race, but an unexpected engine failure forced him to retire from the race with only 2 and a half laps left, leaving 10 points on the table."
hungary_2008.change_text = "Massa hangs on for two more laps to win race (10pts)."
db.session.add(hungary_2008)

belguim_2008 = Race.query.filter(Race.season_year == 2008, Race.abbreviation == 'BEL').first()
belguim_2008.blurb = "In a difficult and eventful race, Hamilton managed to bring home a win, crossing the line in first and even standing on the top step of the podium for the winner's ceremony. But in a highly unusual move, the FIA steward issued a 25 second penalty to Hamilton 2 hours after the race due to cutting a corner and gaining an advantage. This highly controversial decision divided the F1 paddock and led to months of legal court battles but with no different result."
belguim_2008.change_text = "Hamilton gets no controversial penalty, wins race (10pts)."
db.session.add(belguim_2008)

italy_2008 = Race.query.filter(Race.season_year == 2008, Race.abbreviation == 'ITA').first()
italy_2008.blurb = "A poor qualifying and race performance from both Hamilton and Massa left them out of the top 5, scoring just a handful of points. This race did, however, feature Sebastian Vettel becoming the youngest driver to win a Formula 1 race. Vettel would go on to claim the youngest driver to win the Drivers' Championship in 2010 as well."
db.session.add(italy_2008)

japan_2008 = Race.query.filter(Race.season_year == 2008, Race.abbreviation == 'JPN').first()
japan_2008.blurb = "On lap 2, Massa locked-up going into turn 10 and hit Hamilton's car spinning him, forcing him to pit, and dropping Hamilton to 18th. Though Massa was handed a penalty for this, he still finished in 7th with 2 points, while Hamilton finished with no points in 12th. Heading into the final race of the season, then, Hamilton led Massa 94 points to 87 points, a sizable lead since the maximum points available for one race is 10. Even if Massa won, Hamilton would only need 5th place in Brazil to still win the championship."
japan_2008.change_text = "Massa is punished more severely for contact with Hamilton (0pts)."
db.session.add(japan_2008)

brazil_2008 = Race.query.filter(Race.season_year == 2008, Race.abbreviation == 'BRA').first()
brazil_2008.blurb = "The 2008 Brazilian Grand Prix remains perhaps the most dramatic final race of a Formula 1 season.  For the majority of the race Massa led with Hamilton only a few position behind (but enough to win the championship. However, rain began to fall on lap 63 (of 71) and all of the top drivers except Timo Glock pitted for intermediate-weather tires. As a result, Glock moved passed Hamilton into fourth place, demoting Hamilton to 5th (the lowest place where we would still win the championship). On lap 69 (two to the end), Vettel passed Hamilton demoting him to 6th, giving Massa the championship. As Massa passed the finish line, premature celebration erupted in the Ferrari garage and Vettel and then Hamilton passed the struggling Timo Glock around the very final corner of the race, a mere few hundred meters from the finish line, promoting Hamilton to 5th place winning him the championship by 1 point. Although 6th place would have resulted in a tie on points, Massa would have one the championship since he had more race wins."
brazil_2008.change_text = "Hamilton can't fight back to 5th place, finishes 6th (3pts)."
db.session.add(brazil_2008)
# *************************************************************************************************
# *************************************************************************************************


# function for making changes connections
def add_change(season, race, driver, new_pos, new_poi):
    new_change = Change(
        season_year=season,
        race_id=race.id,
        driver_id=driver.id,
        new_position=new_pos,
        new_points=new_poi
    )
    db.session.add(new_change)
    db.session.commit()


# s2007 changes
# find s2007 drivers
RAI = Driver.query.filter_by(code='RAI').first()
HAM = Driver.query.filter_by(code='HAM').first()
ALO = Driver.query.filter_by(code='ALO').first()
MAS = Driver.query.filter_by(code='MAS').first()

# Monaco
add_change(2007, monaco_2007, RAI, 9, 0)

# Canada
add_change(2007, canada_2007, MAS, 2, 8)
add_change(2007, canada_2007, RAI, 6, 3)

# France
add_change(2007, france_2007, ALO, 4, 5)

# Turkey
add_change(2007, turkey_2007, HAM, 2, 8)
add_change(2007, turkey_2007, RAI, 3, 6)
add_change(2007, turkey_2007, ALO, 4, 5)

# Italy
add_change(2007, italy_2007, MAS, 3, 6)
add_change(2007, italy_2007, RAI, 4, 5)

# Japan
add_change(2007, japan_2007, ALO, 2, 8)
add_change(2007, japan_2007, RAI, 4, 5)
add_change(2007, japan_2007, MAS, 7, 2)

# China
add_change(2007, china_2007, HAM, 1, 10)
add_change(2007, china_2007, RAI, 2, 8)
add_change(2007, china_2007, ALO, 3, 6)
add_change(2007, china_2007, MAS, 4, 5)

# Brazil
add_change(2007, brazil_2007, HAM, 1, 10)
add_change(2007, brazil_2007, RAI, 2, 8)
add_change(2007, brazil_2007, ALO, 4, 5)
add_change(2007, brazil_2007, MAS, 3, 6)


# s2010 changes
# find s2010 drivers
VET = Driver.query.filter_by(code='VET').first()
HAM = Driver.query.filter_by(code='HAM').first()
ALO = Driver.query.filter_by(code='ALO').first()
MAS = Driver.query.filter_by(code='MAS').first()
BUT = Driver.query.filter_by(code='BUT').first()
WEB = Driver.query.filter_by(code='WEB').first()

# Austrailia
add_change(2010, austrailia_2010, VET, 1, 25)
add_change(2010, austrailia_2010, ALO, 5, 10)
add_change(2010, austrailia_2010, WEB, 10, 1)
add_change(2010, austrailia_2010, HAM, 7, 6)
add_change(2010, austrailia_2010, BUT, 2, 18)
add_change(2010, austrailia_2010, MAS, 3, 15)

# Malaysia
add_change(2010, malaysia_2010, ALO, 8, 4)
add_change(2010, malaysia_2010, BUT, 9, 2)

# Spain
add_change(2010, spain_2010, HAM, 2, 18)
add_change(2010, spain_2010, VET, 4, 12)
add_change(2010, spain_2010, ALO, 3, 15)
add_change(2010, spain_2010, MAS, 7, 6)

# Turkey
add_change(2010, turkey_2010, WEB, 1, 25)
add_change(2010, turkey_2010, VET, 2, 18)
add_change(2010, turkey_2010, HAM, 3, 15)
add_change(2010, turkey_2010, BUT, 4, 12)
add_change(2010, turkey_2010, ALO, 5, 10)
add_change(2010, turkey_2010, MAS, 8, 4)

# Europe
add_change(2010, europe_2010, WEB, 2, 18)
add_change(2010, europe_2010, ALO, 9, 2)
add_change(2010, europe_2010, HAM, 3, 15)
add_change(2010, europe_2010, BUT, 4, 12)

# Germany
add_change(2010, germany_2010, ALO, 99, 0)
add_change(2010, germany_2010, MAS, 99, 0)

# Hungary
add_change(2010, hungary_2010, HAM, 4, 12)
add_change(2010, hungary_2010, MAS, 5, 10)
add_change(2010, hungary_2010, BUT, 9, 2)

# Italy
add_change(2010, italy_2010, HAM, 5, 10)
add_change(2010, italy_2010, WEB, 7, 6)

# Singapore
add_change(2010, singapore_2010, HAM, 3, 15)
add_change(2010, singapore_2010, WEB, 4, 12)
add_change(2010, singapore_2010, BUT, 5, 10)
add_change(2010, singapore_2010, MAS, 9, 2)

# Korea
add_change(2010, korea_2010, VET, 1, 25)
add_change(2010, korea_2010, ALO, 2, 18)
add_change(2010, korea_2010, HAM, 3, 15)



# 2008
# s2008 changes
# find s2008 drivers
HAM = Driver.query.filter_by(code='HAM').first()
MAS = Driver.query.filter_by(code='MAS').first()

# Austrailia
add_change(2008, austrailia_2008, MAS, 4, 5)

# Malaysia
add_change(2008, malaysia_2008, HAM, 6, 3)
add_change(2008, malaysia_2008, MAS, 5, 4)

# Bahrain
add_change(2008, bahrain_2008, HAM, 3, 6)

# Canada
add_change(2008, canada_2008, HAM, 3, 6)

# Franch
add_change(2008, france_2008, HAM, 3, 6)

# hungary
add_change(2008, hungary_2008, HAM, 6, 3)
add_change(2008, hungary_2008, MAS, 1, 10)

# belgium
add_change(2008, belguim_2008, HAM, 1, 10)
add_change(2008, belguim_2008, MAS, 2, 8)

# Japan
add_change(2008, japan_2008, MAS, 9, 0)

# brazil
add_change(2008, brazil_2008, HAM, 6, 3)


# **********************
#Commit all
db.session.commit()