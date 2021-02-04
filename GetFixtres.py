import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time 

def scrape(cells):
    cell_contents = []
    for cell in cells:
        text = cell.text.strip()
        cell_contents.append(text)
    return (cell_contents)


def get_numbers(string):
    string = string[-4:]

    return string

def get_fixtures(url):
    
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table')
    cells = table.find_all("td")

    output = scrape(cells)

    output = np.array(output)
    output = output.reshape(21, 8)
    output = pd.DataFrame(output)
    header_row = 0
    output.columns = output.iloc[header_row]
    output = output.drop(header_row)
    output = output.reset_index(drop=True)
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

    EG = output
    EG.total = EG.total.apply(float)

    return(output)

EG_data = get_fixtures("https://playerdatabase247.com/include_premier_league_fixture_tracker_uusi.php?listtype=expgoals")
EG_data.name = 'Expected goals'
ECS_data = get_fixtures("https://playerdatabase247.com/include_premier_league_fixture_tracker_uusi.php?listtype=cs")
ECS_data.name = 'Expected clean sheets'

def plot_fixture_data(df):
    fig, ax = plt.subplots(figsize = (25,8))
    fig.tight_layout()
    fig.patch.set_facecolor('#E8E5DA')
    ax.bar(df.team, df.total, color = "#304C89")
    ax.bar(df.team, df.gw1+df.gw2+df.gw3, color = "#648DE5")
    ax.bar(df.team, df.gw1, color = "#9EB7E5")
    ax.set_ylabel("{} (Upcoming gameweek, three week, and six week total)".format(df.name), size = 12)
    plt.xticks(rotation = 30)
    ax.set_facecolor('#E8E5DA')
    plt.savefig('static/images/plot_for_{}.png'.format(df.name),bbox_inches = 'tight', facecolor=fig.get_facecolor())
    return 

#fig size for insta = (25,8) and for website = (15,8)




    

