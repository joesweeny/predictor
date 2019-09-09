import numpy as np
import pandas as pd
from compiler.data.calculation import elo


def apply_current_elo_ratings_for_fixture(fixture: pd.DataFrame, data: pd.DataFrame, points: int) -> pd.DataFrame:
    """
    Calculate and apply home and defence ratings for a Fixture
    """
    row = fixture.iloc[0, :]

    home_rows = data[data['homeTeam'] == row['homeTeam']]
    away_rows = data[data['awayTeam'] == row['awayTeam']]

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
    fixture['awayDefenceStrength'] = away_defence
    fixture['awayDefenceStrength'] = away_defence

    return fixture


def apply_historic_elo_ratings(df, historic_elos, soft_reset_factor, goal_points: int) -> pd.DataFrame:
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
        match_id = row['matchID']

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
        homeElo=lambda frame: frame.matchID.map(match_elos).str[0],
        awayElo=lambda frame: frame.matchID.map(match_elos).str[1],
        homeAttackStrength=lambda frame: frame.matchID.map(match_home_strength).str[0],
        homeDefenceStrength=lambda frame: frame.matchID.map(match_home_strength).str[1],
        awayAttackStrength=lambda frame: frame.matchID.map(match_away_strength).str[0],
        awayDefenceStrength=lambda frame: frame.matchID.map(match_away_strength).str[1],
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
