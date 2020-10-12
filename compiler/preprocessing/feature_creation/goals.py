import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from compiler.preprocessing.calculation import elo

GOAL_POINTS = 20

FEATURE_COLUMNS = [
    "round",
    "homeShotsOnGoalF",
    "homeShotsTotalF",
    "homeShotsOnGoalA",
    "homeShotsTotalA",
    "homeGoalsScored",
    "homeGoalsConceded",
    "homeXGF",
    "homeXGA",
    "awayShotsOnGoalF",
    "awayShotsTotalF",
    "awayShotsOnGoalA",
    "awayShotsTotalA",
    "awayGoalsScored",
    "awayGoalsConceded",
    "awayXGF",
    "awayXGA",
    "homeAttackStrength",
    "homeDefenceStrength",
    "awayAttackStrength",
    "awayDefenceStrength"
]


def process_fixture_data(fixture: pd.Series, results: pd.DataFrame) -> np.array:
    combined = results.append(fixture).fillna(0)

    multi_line = __create_multi_line_stats(combined)

    stats = __create_rolling_stats(multi_line, fixture['season'])

    fixture_rows = __create_fixture_rows(stats)

    ratings = __apply_historic_elo_ratings(
        df=combined,
        historic_elos={team: 1500 for team in combined['homeTeam'].unique()},
        soft_reset_factor=0.96,
        goal_points=GOAL_POINTS
    )

    columns = ['fixtureID', 'homeAttackStrength', 'homeDefenceStrength', 'awayAttackStrength', 'awayDefenceStrength']

    arr = fixture_rows.merge(ratings[columns], on='fixtureID', how='left')

    data = __scale_attributes(arr)

    return data[-1:].to_numpy()


def __scale_attributes(df: pd.DataFrame):
    con = MinMaxScaler().fit_transform(df[FEATURE_COLUMNS])

    return pd.DataFrame(data=con, columns=FEATURE_COLUMNS)


def __create_fixture_rows(df):
    home_columns = {
        "team": "homeTeam",
        "shotsOnGoalF": "homeShotsOnGoalF",
        "shotsTotalF": "homeShotsTotalF",
        "goalsScored": "homeGoalsScored",
        "goalsConceded": "homeGoalsConceded",
        "xGFor": "homeXGF",
        "xGAgainst": "homeXGA",
        "shotsOnGoalA": "homeShotsOnGoalA",
        "shotsTotalA": "homeShotsTotalA",
    }

    away_columns = {
        "team": "awayTeam",
        "shotsOnGoalF": "awayShotsOnGoalF",
        "shotsTotalF": "awayShotsTotalF",
        "goalsScored": "awayGoalsScored",
        "goalsConceded": "awayGoalsConceded",
        "xGFor": "awayXGF",
        "xGAgainst": "awayXGA",
        "shotsOnGoalA": "awayShotsOnGoalA",
        "shotsTotalA": "awayShotsTotalA",
    }

    home = df[df["atHome"] == 1].rename(columns=home_columns)
    away = df[df["atHome"] == 0].rename(columns=away_columns)

    merged = home.merge(away, on=["fixtureID", "date", "season", "round"], how='left')

    return merged.drop(columns=["atHome_x", "atHome_y"])


def __create_rolling_stats(df: pd.DataFrame, season: str) -> pd.DataFrame:
    df = df[df['season'] == season]

    core_columns = ['fixtureID', 'date', 'round', 'season', 'team', 'atHome']

    core_features = df[core_columns].copy()

    feature_names = df.drop(columns=core_columns).columns

    for feature_name in feature_names:
        stat = df.groupby(['team'])[feature_name].apply(lambda x: x.shift().cumsum())
        core_features[feature_name] = round(stat, 2)

    return core_features


def __create_multi_line_stats(df: pd.DataFrame) -> pd.DataFrame:
    home_columns = [
        'homeTeam',
        'homeGoals',
        'homeXG',
        'homeShotsOnGoal',
        'homeShotsTotal',
        'awayGoals',
        'awayXG',
        'awayShotsOnGoal',
        'awayShotsTotal',
    ]

    away_columns = [
        'awayTeam',
        'awayGoals',
        'awayXG',
        'awayShotsOnGoal',
        'awayShotsTotal',
        'homeGoals',
        'homeXG',
        'homeShotsOnGoal',
        'homeShotsTotal',
    ]

    column_mappings = [
        'team',
        'goalsScored',
        'xGFor',
        'shotsOnGoalF',
        'shotsTotalF',
        'goalsConceded',
        'xGAgainst',
        'shotsOnGoalA',
        'shotsTotalA',
    ]

    home_mapping = {old_column: new_column for old_column, new_column in zip(home_columns, column_mappings)}
    away_mapping = {old_column: new_column for old_column, new_column in zip(away_columns, column_mappings)}

    multi_line = (df[['fixtureID', 'date', 'round', 'season'] + home_columns]
                  .rename(columns=home_mapping)
                  .assign(atHome=1)
                  .append((df[['fixtureID', 'date', 'round', 'season'] + away_columns])
                          .rename(columns=away_mapping)
                          .assign(atHome=0), sort=True)
                  .sort_values(by=['date', 'fixtureID'])
                  .reset_index(drop=True))

    return multi_line


def __apply_current_elo_ratings_for_fixture(fixture: pd.Series, data: pd.DataFrame, points: int) -> pd.Series:
    """
    Calculate and apply home and defence ratings for a Fixture
    """
    home_rows = data[data['homeTeam'] == fixture['homeTeam']]
    away_rows = data[data['awayTeam'] == fixture['awayTeam']]

    home = home_rows.iloc[-1, :]
    away = away_rows.iloc[-1, :]

    home_attack, _ = elo.calculate_attack_and_defence_ratings(
        points,
        home['homeAttackStrength'],
        home['awayDefenceStrength'],
        home['homeGoals']
    )

    _, home_defence = elo.calculate_attack_and_defence_ratings(
        points,
        home['awayAttackStrength'],
        home['homeDefenceStrength'],
        home['awayGoals']
    )

    away_attack, _ = elo.calculate_attack_and_defence_ratings(
        points,
        away['awayAttackStrength'],
        away['homeDefenceStrength'],
        away['awayGoals']
    )

    _, away_defence = elo.calculate_attack_and_defence_ratings(
        points,
        away['homeAttackStrength'],
        away['awayDefenceStrength'],
        away['homeGoals']
    )

    fixture['homeAttackStrength'] = home_attack
    fixture['homeDefenceStrength'] = home_defence
    fixture['awayAttackStrength'] = away_attack
    fixture['awayDefenceStrength'] = away_defence

    return fixture


def __apply_historic_elo_ratings(df, historic_elos, soft_reset_factor, goal_points: int) -> pd.DataFrame:
    """
    Calculate rolling ELO ratings for teams based on results provided in data frame
    """
    # Initialise a dictionary with default elos for each team
    for team in df['homeTeam'].unique():
        if team not in historic_elos.keys():
            historic_elos[team] = 1500

    current_elos = historic_elos.copy()
    current_home_attack_elos = historic_elos.copy()
    current_home_defence_elos = historic_elos.copy()
    current_away_attack_elos = historic_elos.copy()
    current_away_defence_elos = historic_elos.copy()
    match_elos = {}
    match_home_strength = {}
    match_away_strength = {}

    last_season = 0

    # Loop over the rows in the DataFrame
    for index, row in df.iterrows():
        # Get the current year
        current_season = row['season']

        # If it is a new season, soft-reset elos
        if current_season != last_season:
            current_elos = __revert_elos_to_mean(current_elos, soft_reset_factor)
            current_home_attack_elos = __revert_elos_to_mean(current_home_attack_elos, soft_reset_factor)
            current_home_defence_elos = __revert_elos_to_mean(current_home_defence_elos, soft_reset_factor)
            current_away_attack_elos = __revert_elos_to_mean(current_away_attack_elos, soft_reset_factor)
            current_away_defence_elos = __revert_elos_to_mean(current_away_defence_elos, soft_reset_factor)

        # Get the Game ID
        match_id = row['fixtureID']

        # Get the team and opposition
        home_team = row['homeTeam']
        away_team = row['awayTeam']

        # Get the team and opposition elo score
        home_team_elo = current_elos[home_team]
        away_team_elo = current_elos[away_team]
        home_attack_elo = current_home_attack_elos[home_team]
        home_defence_elo = current_home_defence_elos[home_team]
        away_attack_elo = current_away_attack_elos[away_team]
        away_defence_elo = current_away_defence_elos[away_team]

        # Add the elos and probabilities our elos dictionary and elo_probs dictionary based on the Match ID
        match_elos[match_id] = [home_team_elo, away_team_elo]
        match_home_strength[match_id] = [home_attack_elo, home_defence_elo]
        match_away_strength[match_id] = [away_attack_elo, away_defence_elo]

        # Calculate the new elos of each team
        new_home_team_elo, new_away_team_elo = elo.calculate_team_ratings(
            25,
            home_team_elo,
            away_team_elo,
            row['homeGoals'],
            row['awayGoals']
        )

        new_home_attack, new_away_defence = elo.calculate_attack_and_defence_ratings(
            goal_points,
            home_attack_elo,
            away_defence_elo,
            row['homeGoals']
        )

        new_away_attack, new_home_defence = elo.calculate_attack_and_defence_ratings(
            goal_points,
            away_attack_elo,
            home_defence_elo,
            row['awayGoals']
        )

        # Update elos in elo dictionary
        current_elos[home_team] = new_home_team_elo
        current_elos[away_team] = new_away_team_elo
        current_home_attack_elos[home_team] = new_home_attack
        current_away_attack_elos[away_team] = new_away_attack
        current_home_defence_elos[home_team] = new_home_defence
        current_away_defence_elos[away_team] = new_away_defence

        last_season = current_season

    updated = (df.assign(
        homeElo=lambda frame: frame.fixtureID.map(match_elos).str[0],
        awayElo=lambda frame: frame.fixtureID.map(match_elos).str[1],
        homeAttackStrength=lambda frame: frame.fixtureID.map(match_home_strength).str[0],
        homeDefenceStrength=lambda frame: frame.fixtureID.map(match_home_strength).str[1],
        awayAttackStrength=lambda frame: frame.fixtureID.map(match_away_strength).str[0],
        awayDefenceStrength=lambda frame: frame.fixtureID.map(match_away_strength).str[1],
    ))

    return updated


def __revert_elos_to_mean(current_elos, soft_reset_factor):
    """
    Soft reset ELOs when a new seasons data is provided
    """
    elos_mean = np.mean(list(current_elos.values()))

    new_elos_dict = {
        team: (team_elo - elos_mean) * soft_reset_factor + elos_mean for team, team_elo in current_elos.items()
    }

    return new_elos_dict
