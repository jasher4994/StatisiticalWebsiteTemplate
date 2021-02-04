import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2020-21/players_raw.csv")
df["position"] = df["element_type"]
df.position = df.position.replace([1,2,3,4], ["GK", "DEF", "MID", "FWD"])
df.now_cost = df.now_cost/10


"""roi"""
roi = df.loc[:, ["web_name", "position", "total_points", "now_cost", "team"]]
roi["roi"] = roi["total_points"]/roi["now_cost"]
roi = roi.sort_values(by = "roi", ascending = False)

roi.team = roi.team.replace([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
                ["Arsenal", "Aston Villa", "Brighton", "Burnley", "Chelsea", 
                "Crystal Palace", "Everton", "Fulham", "Leicester", "Leeds",
                "Liverpool", "Manchester City", "Manchester United",
                "Newcastle", "Sheffield Utd", "Southampton", "Tottenham",
                "West Brom", "West Ham", "Wolverhampton"])

roi_GK = roi[roi.position == "GK"]
roi_GK = roi_GK.iloc[0:10, :]

roi_DEF = roi[roi.position == "DEF"]
roi_DEF = roi_DEF.iloc[0:10, :]

roi_MID = roi[roi.position == "MID"]
roi_MID = roi_MID.iloc[0:10, :]

roi_FWD = roi[roi.position == "FWD"]
roi_FWD = roi_FWD.iloc[0:10, :]

url = "https://playerdatabase247.com/include_premier_league_fixture_tracker_uusi.php?listtype=expgoals"
r = requests.get(url)
#print(r.status_code)

soup = BeautifulSoup(r.text, 'html.parser')
table = soup.find('table')
cells = table.find_all("td")

def scrape(cells):
    lizt = []
    for cell in cells:
        text = cell.text.strip()
        lizt.append(text)
    return(lizt)
    
output = scrape(cells)

output = np.array(output)
output = output.reshape(21,8)
output = pd.DataFrame(output)
header_row = 0
output.columns = output.iloc[header_row]
output = output.drop(header_row)
output = output.reset_index(drop = True)
output.columns = ["team", "gw1", "gw2", "gw3", "gw4", "gw5", "gw6", "total"]

def get_numbers(string):
    string = string[-4:]

    return string

output.gw1 = output.gw1.apply(get_numbers)
output.gw1 = output.gw1.apply(float)
output.gw2 = output.gw2.apply(get_numbers)
output.gw2 = output.gw2.apply(float)
output.gw3 = output.gw3.apply(get_numbers)
output.gw3 = output.gw3.apply(float)
output.gw4 = output.gw4.apply(get_numbers)
output.gw4 = output.gw4.apply(float)
output.gw5 = output.gw5.apply(get_numbers)
output.gw5 = output.gw5.apply(float)
output.gw6 = output.gw6.apply(get_numbers)
output.gw6 = output.gw6.apply(float)
EG = output

url = "https://playerdatabase247.com/include_premier_league_fixture_tracker_uusi.php?listtype=cs"

r = requests.get(url)
#print(r.status_code)

soup = BeautifulSoup(r.text, 'html.parser')
table = soup.find('table')
cells = table.find_all("td")

output = scrape(cells)

output = np.array(output)
output = output.reshape(21,8)
output = pd.DataFrame(output)
header_row = 0
output.columns = output.iloc[header_row]
output = output.drop(header_row)
output = output.reset_index(drop = True)
output.columns = ["team", "gw1", "gw2", "gw3", "gw4", "gw5", "gw6", "total"]

output.gw1 = output.gw1.apply(get_numbers)
output.gw1 = output.gw1.apply(float)
output.gw2 = output.gw2.apply(get_numbers)
output.gw2 = output.gw2.apply(float)
output.gw3 = output.gw3.apply(get_numbers)
output.gw3 = output.gw3.apply(float)
output.gw4 = output.gw4.apply(get_numbers)
output.gw4 = output.gw4.apply(float)
output.gw5 = output.gw5.apply(get_numbers)
output.gw5 = output.gw5.apply(float)
output.gw6 = output.gw6.apply(get_numbers)
output.gw6 = output.gw6.apply(float)
ECS = output

EG["EG - one week"] = EG.gw1
EG["EG - three week"] = EG.gw1 + EG.gw2 + EG.gw3
EG["EG - six week"] = EG.total
EG = EG.iloc[:,[0,8,9,10]]

ECS["ECS - one week"] = ECS.gw1
ECS["ECS - three week"] = ECS.gw1 + ECS.gw2 + ECS.gw3
ECS["ECS - six week"] = ECS.total
ECS = ECS.iloc[:,[0,8,9,10]]

full_df = pd.merge(roi,EG, on = "team")
full_df = pd.merge(full_df, ECS, on = "team")

full_df = full_df.sort_values(by = "roi", ascending = False)


float_cols = ['total_points', 'now_cost','roi',
       'EG - one week', 'EG - three week', 'EG - six week', 'ECS - one week',
       'ECS - three week', 'ECS - six week', 'ECS - one week',
       'ECS - three week', 'ECS - six week']

for i in float_cols:
    full_df[i] = pd.to_numeric(full_df[i])
    
GK = full_df[full_df.position == "GK"]
GK_roi = GK.iloc[0:20,:]
GK_roi.columns = ["Name", "Position", "Points", "Cost", "Team", "ROI", "EG(1)", "EG(3)", "EG(6)", "ECS(1)", "ECS(3)", "ECS(6)"]
GK_roi = GK_roi.drop(columns = ["EG(1)", "EG(3)", "EG(6)"])

DEF = full_df[full_df.position == "DEF"]
DEF_roi = DEF.iloc[0:15,:]
DEF_roi.columns = ["Name", "Position", "Points", "Cost", "Team", "ROI", "EG(1)", "EG(3)", "EG(6)", "ECS(1)", "ECS(3)", "ECS(6)"]
DEF_roi = DEF_roi.drop(columns = ["EG(1)", "EG(3)", "EG(6)"])

MID = full_df[full_df.position == "MID"]
MID_roi = MID.iloc[0:15,:]
MID_roi.columns = ["Name", "Position", "Points", "Cost", "Team", "ROI", "EG(1)", "EG(3)", "EG(6)", "ECS(1)", "ECS(3)", "ECS(6)"]
MID_roi = MID_roi.drop(columns = ["ECS(1)", "ECS(3)", "ECS(6)"])

FWD = full_df[full_df.position == "FWD"]
FWD_roi = FWD.iloc[0:15,:]
FWD_roi.columns = ["Name", "Position", "Points", "Cost", "Team", "ROI", "EG(1)", "EG(3)", "EG(6)", "ECS(1)", "ECS(3)", "ECS(6)"]
FWD_roi = FWD_roi.drop(columns = ["ECS(1)", "ECS(3)", "ECS(6)"])
