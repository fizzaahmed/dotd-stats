import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_url(year, gp_name):
    gp_name_underscored = gp_name.replace(" ", "_")
    return f'https://f1.fandom.com/wiki/{year}_{gp_name_underscored}'

def get_race_table(year, gp_name):
    # get page
    URL = get_url(year, gp_name)
    page = requests.get(URL)

    # find tables in page
    tables = pd.read_html(page.text)

    # find the race table and return it
    race_table = pd.DataFrame()
    columns = ["Pos.", "No.", "Driver", "Constructor", "Laps", "Time/Retired", "Grid", "Points"]
    columns_v2 = ["Pos.", "No.", "Driver", "Constructor", "Laps", "Time/Retired", "Grid", "Pts."]
    columns_v3 = ['Pos.', 'No.', 'Driver', 'Constructor', 'Laps', 'Time/Retired', 'Grid', 'Points', 'Unnamed: 8']        
    for table in tables:
        if table.columns.tolist() == columns or table.columns.tolist() == columns_v2 or table.columns.tolist() == columns_v3:
            race_table = table
    return race_table

def get_position_of_dotd(dotd):
    year, gp_name, driver = dotd["Year"], dotd["Race Name"], dotd["Driver"]
    print(f'year {year} gp_name {gp_name} driver {driver}')
    try:
        race_table = get_race_table(year, gp_name)
        position = race_table[race_table["Driver"] == driver]["Pos."]
        return position.tolist()[0]
    except KeyError as e:
        return "FIND MANUALLY"
    except IndexError as e:
        return "FIND MANUALLY"



# read in csv
# dotds = pd.read_csv("dotd_stats_full.csv", dtype=str)
# #dotds = pd.read_csv("dotd_sample.csv", dtype=str)

# # apply function to get position for each driver to the dataframe
# dotds["Position"] = dotds.apply(get_position_of_dotd, axis=1)
# #print(dotds)

# # save to csv
# dotds.to_csv('dotd_stats_full_with_pos.csv', index=False)

def get_championship_position(year, gp_name):
    # get page
    URL = get_url(year, gp_name)
    page = requests.get(URL)

    # find tables in page
    tables = pd.read_html(page.text)

    # find the race table and return it
    champ_table = pd.DataFrame()
    columns = [("Drivers' World Championship", 'Pos.'), ("Drivers' World Championship", 'Driver'), ("Drivers' World Championship", 'Pts.'), ("Drivers' World Championship", '+/-')]
    columns_v2 = [("Drivers' World Championship", 'Pos'), ("Drivers' World Championship", 'Driver'), ("Drivers' World Championship", 'Pts'), ("Drivers' World Championship", '+/-')]
    columns_v3 = [("Drivers' World Championship", 'Pos.'), ("Drivers' World Championship", 'Driver'), ("Drivers' World Championship", 'Pts'),  ('Unnamed: 3_level_0', 'Unnamed: 3_level_1'), ('Unnamed: 4_level_0', 'Unnamed: 4_level_1')]
    for table in tables:
        # print(table.columns.tolist())
        if table.columns.tolist()[0] == columns[0] or table.columns.tolist()[0] == columns_v2[0]:# or table.columns.tolist() == columns_v3:
            champ_table = table
    return champ_table

def get_champ_position_of_dotd(dotd):
    year, gp_name, driver = dotd["Year"], dotd["Race Name"], dotd["Driver"]
    print(f'year {year} gp_name {gp_name} driver {driver}')
    try:
        champ_table = get_championship_position(year, gp_name)
        driver_col = champ_table.columns.tolist()[1]
        position_col = champ_table.columns.tolist()[0]
        position = champ_table[champ_table[driver_col] == driver][position_col]
        return position.tolist()[0]
    except KeyError as e:
        print("FIND MANUALLY")
        return "FIND MANUALLY"
    except IndexError as e:
        print("FIND MANUALLY")
        return "FIND MANUALLY"
    
dotds = pd.read_csv("dotd_stats_full_with_pos.csv", dtype=str)
#dotds = pd.read_csv("dotd_sample.csv", dtype=str)
    
dotds["Championship Standing"] = dotds.apply(get_champ_position_of_dotd, axis=1)
print(dotds.head())
dotds.to_csv('dotd_stats_full_with_pos_and_champ.csv', index=False)


