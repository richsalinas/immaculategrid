import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

# Reading Lahman databases
people = pd.read_csv("website/static/lahman_1871-2023_csv/People.csv", encoding = 'latin-1')
people = people[people['debut'].notna()]
appearances = pd.read_csv("website/static/lahman_1871-2023_csv/Appearances.csv", encoding = 'latin-1')
teams = pd.read_csv("website/static/lahman_1871-2023_csv/Teams.csv", encoding = 'latin-1')

# Function to call current franchises and their IDs
def franch_df():
    franch_ids = list(teams.loc[teams['yearID'] == 2023, 'franchID'])
    franch_names = [
            "Baltimore Orioles", "Boston Red Sox", "Chicago White Sox", "Cleveland Guardians",
            "Detroit Tigers", "Houston Astros", "Kansas City Royals", "Los Angeles Angels",
            "Minnesota Twins", "New York Yankees", "Oakland Athletics", "Seattle Mariners",
            "Tampa Bay Rays", "Texas Rangers", "Toronto Blue Jays", "Arizona Diamondbacks",
            "Atlanta Braves", "Chicago Cubs", "Cincinnati Reds", "Colorado Rockies",
            "Los Angeles Dodgers", "Miami Marlins", "Milwaukee Brewers", "New York Mets",
            "Philadelphia Phillies", "Pittsburgh Pirates", "San Diego Padres", "San Francisco Giants",
            "St. Louis Cardinals", "Washington Nationals"
            ]

    return pd.DataFrame({
        'franch_id': franch_ids,
        'franch_names': franch_names,
        'franch_src': ['/logos/' + id + '.png' for id in franch_ids]
    })

# Function to call a dataframe that contains a player's ID, full name, and years played
def player_names():
    player_names = people[['playerID', 'nameFirst', 'nameLast']]
    player_names['full_name'] = player_names['nameFirst'] + " " + player_names['nameLast']
    player_names['debut'] = [x.split("-")[0] for x in list(people['debut'])]
    player_names['endyear'] = [x.split("-")[0] for x in list(people['finalGame'])]
    player_names['search_option'] = player_names['full_name'] + " (" + player_names['debut'] + "-" + player_names['endyear'] + ")"

    return player_names[['playerID', 'full_name', 'search_option']]


# Function to check if chosen player played for specific teams
def on_teams(team_one, team_two, player):
    teams_played = pd.unique(appearances[appearances['playerID'] == player]['teamID'])

    # Translate team IDs into current franchise IDs
    for idx in range(len(teams_played)):
        teams_played[idx] = pd.unique(teams[teams['teamID'] == teams_played[idx]]['franchID'])[-1]

    if team_one in teams_played and team_two in teams_played:
        return True
    else:
        return False

# Return player ID based on given full name
def get_player_id(name):
    return player_names()[player_names()['search_option'] == name]['playerID'].values[0]