race_abbrs = {
    'race_abbrs_2007' : {
        'Australian Grand Prix': 'AUS',
        'Malaysian Grand Prix': 'MAL',
        'Bahrain Grand Prix': 'BHR',
        'Spanish Grand Prix': 'ESP',
        'Monaco Grand Prix': 'MON',
        'Canadian Grand Prix': 'CAN',
        'United States Grand Prix': 'USA',
        'French Grand Prix': 'FRA',
        'British Grand Prix': 'GBR',
        'European Grand Prix': 'EUR',
        'Hungarian Grand Prix': 'HUN',
        'Turkish Grand Prix': 'TUR',
        'Italian Grand Prix': 'ITA',
        'Belgian Grand Prix': 'BEL',
        'Japanese Grand Prix': 'JPN',
        'Chinese Grand Prix': 'CHN',
        'Brazilian Grand Prix': 'BRA'
    },
    'race_abbrs_1984' : {
        'Brazilian Grand Prix': 'BRA',
        'South African Grand Prix': 'RSA',
        'Belgian Grand Prix': 'BEL',
        'San Marino Grand Prix': 'SMR',
        'French Grand Prix': 'FRA',
        'Monaco Grand Prix': 'MON',
        'Canadian Grand Prix': 'CAN',
        'Detroit Grand Prix': 'DET',
        'Dallas Grand Prix': 'DAL',
        'British Grand Prix': 'GBR',
        'German Grand Prix': 'GER',
        'Austrian Grand Prix': 'AUT',
        'Dutch Grand Prix': 'NED',
        'Italian Grand Prix': 'ITA',
        'European Grand Prix': 'EUR',
        'Portuguese Grand Prix': 'POR'
    },
    'race_abbrs_2010' : {
        'Bahrain Grand Prix': 'BHR',
        'Australian Grand Prix': 'AUS',
        'Malaysian Grand Prix': 'MAL',
        'Chinese Grand Prix': 'CHN',
        'Spanish Grand Prix': 'ESP',
        'Monaco Grand Prix': 'MON',
        'Turkish Grand Prix': 'TUR',
        'Canadian Grand Prix': 'CAN',
        'European Grand Prix': 'EUR',
        'British Grand Prix': 'GBR',
        'German Grand Prix': 'GER',
        'Hungarian Grand Prix': 'HUN',
        'Belgian Grand Prix': 'BEL',
        'Italian Grand Prix': 'ITA',
        'Singapore Grand Prix': 'SIN',
        'Japanese Grand Prix': 'JPN',
        'Korean Grand Prix': 'KOR',
        'Brazilian Grand Prix': 'BRA',
        'Abu Dhabi Grand Prix': 'ABU'
    },
    'race_abbrs_2008' : {
        'Australian Grand Prix': 'AUS',
        'Malaysian Grand Prix': 'MAL',
        'Bahrain Grand Prix': 'BHR',
        'Spanish Grand Prix': 'ESP',
        'Turkish Grand Prix': 'TUR',
        'Monaco Grand Prix': 'MON',
        'Canadian Grand Prix': 'CAN',
        'French Grand Prix': 'FRA',
        'British Grand Prix': 'GBR',
        'German Grand Prix': 'GER',
        'Hungarian Grand Prix': 'HUN',
        'European Grand Prix': 'EUR',
        'Belgian Grand Prix': 'BEL',
        'Italian Grand Prix': 'ITA',
        'Singapore Grand Prix': 'SIN',
        'Japanese Grand Prix': 'JPN',
        'Chinese Grand Prix': 'CHN',
        'Brazilian Grand Prix': 'BRA'
    },
    'race_abbrs_2021' : {
        'Bahrain Grand Prix': 'BHR',
        'Emilia Romagna Grand Prix': 'EMI',
        'Portuguese Grand Prix': 'POR',
        'Spanish Grand Prix': 'ESP',
        'Monaco Grand Prix': 'MON',
        'Azerbaijan Grand Prix': 'AZE',
        'French Grand Prix': 'FRA',
        'Styrian Grand Prix': 'STY',
        'Austrian Grand Prix': 'AUT',
        'British Grand Prix': 'GBR',
        'Hungarian Grand Prix': 'HUN',
        'Belgian Grand Prix': 'BEL',
        'Dutch Grand Prix': 'NED',
        'Italian Grand Prix': 'ITA',
        'Russian Grand Prix': 'RUS',
        'Turkish Grand Prix': 'TUR',
        'United States Grand Prix': 'USA',
        'Mexico City Grand Prix': 'MXC',
        'São Paulo Grand Prix': 'SAP',
        'Qatar Grand Prix': 'QAT',
        'Saudi Arabian Grand Prix': 'SAU',
        'Abu Dhabi Grand Prix': 'ABU'
    }
}

# Code to quickly print dictionary of given seasons race names:
# Abbreviations then styled after the f1 wikipedia

# import requests
# race_abbrs = {}

# resp = requests.get("https://ergast.com/api/f1/2008.json?limit=30")

# r_json = resp.json()

# races = r_json['MRData']['RaceTable']['Races']

# for race in races:
#     r_name = race['raceName']
#     race_abbrs[r_name] = ''

# print(race_abbrs)