import numpy as np
import pandas as pd
from typing import List


def append_and_sort_by_column(dfs: List[pd.DataFrame], col: str, asc: bool) -> pd.DataFrame:
    """
    Combine all Pandas data frames passed as first argument and sort by column provided
    """
    combined = pd.concat(dfs)
    combined.sort_values(by=[col], inplace=True, ascending=asc)
    combined = combined.reset_index(drop=True)

    return combined


def create_over_goals_target_variable_column(df: pd.DataFrame, goals: float) -> pd.DataFrame:
    """
    Create a Over X Amount Goals target variable column based on second argument provided
    """
    col = 'over' + str(goals) + 'Goals'
    df[col] = np.where(df['homeGoals'] + df['awayGoals'] > goals, 1, 0)

    return df


def elo_calculator(df, k_factor, historic_elos, soft_reset_factor, match_id_column):
    """
    Calculate rolling ELO ratings for teams based on results provided in dataframe
    """
    # Initialise a dictionary with default elos for each team
    for team in df['homeTeam'].unique():
        if team not in historic_elos.keys():
            historic_elos[team] = 1500

    elo_current = historic_elos.copy()
    elos, elo_probs = {}, {}

    last_season = 0

    # Loop over the rows in the DataFrame
    for index, row in df.iterrows():
        # Get the current year
        current_season = row['season']

        # If it is a new season, soft-reset elos
        if current_season != last_season:
            elo_current = __revert_elos_to_mean(elo_current, soft_reset_factor)

        # Get the Game ID
        match_id = row[match_id_column]

        # Get the team and opposition
        home_team = row['homeTeam']
        away_team = row['awayTeam']

        # Get the team and opposition elo score
        home_team_elo = elo_current[home_team]
        away_team_elo = elo_current[away_team]

        # Calculated the probability of winning for the team and opposition
        prob_win_home = 1 / (1 + 10 ** ((away_team_elo - home_team_elo) / 400))
        prob_win_away = 1 - prob_win_home

        # Add the elos and probabilities our elos dictionary and elo_probs dictionary based on the Match ID
        elos[match_id] = [round(home_team_elo, 2), round(away_team_elo, 2)]
        elo_probs[match_id] = [round(prob_win_home, 2), round(prob_win_away, 2)]

        margin = row['homeGoals'] - row['awayGoals']

        new_home_team_elo = home_team_elo
        new_away_team_elo = away_team_elo

        # Calculate the new elos of each team
        if margin == 1:  # Team wins; update both teams' elo
            new_home_team_elo = home_team_elo + k_factor * (1 - prob_win_home) * 1
            new_away_team_elo = away_team_elo + k_factor * (0 - prob_win_away) * 1
        elif margin == 2:
            new_home_team_elo = home_team_elo + k_factor * (1 - prob_win_home) * 1.5
            new_away_team_elo = away_team_elo + k_factor * (0 - prob_win_away) * 1.5
        elif margin == 3:
            new_home_team_elo = home_team_elo + k_factor * (1 - prob_win_home) * 1.75
            new_away_team_elo = away_team_elo + k_factor * (0 - prob_win_away) * 1.75
        elif margin > 3:
            new_home_team_elo = home_team_elo + k_factor * (1 - prob_win_home) * 1.75 * (margin - 3) / 8
            new_away_team_elo = away_team_elo + k_factor * (0 - prob_win_away) * 1.75 * (margin - 3) / 8
        elif margin == -1:  # Away team wins; update both teams' elo
            new_home_team_elo = home_team_elo + k_factor * (0 - prob_win_home) * 1
            new_away_team_elo = away_team_elo + k_factor * (1 - prob_win_away) * 1
        elif margin == -2:  # Away team wins; update both teams' elo
            new_home_team_elo = home_team_elo + k_factor * (0 - prob_win_home) * 1.5
            new_away_team_elo = away_team_elo + k_factor * (1 - prob_win_away) * 1.5
        elif margin == -3:  # Away team wins; update both teams' elo
            new_home_team_elo = home_team_elo + k_factor * (0 - prob_win_home) * 1.75
            new_away_team_elo = away_team_elo + k_factor * (1 - prob_win_away) * 1.75
        elif margin < -3:  # Away team wins; update both teams' elo
            new_home_team_elo = home_team_elo + k_factor * (0 - prob_win_home) * 1.75 * (margin - 3) / 8
            new_away_team_elo = away_team_elo + k_factor * (1 - prob_win_away) * 1.75 * (margin - 3) / 8
        elif margin == 0:  # Drawn game' update both teams' elo
            new_home_team_elo = home_team_elo + k_factor * (0.5 - prob_win_home) * 1
            new_away_team_elo = away_team_elo + k_factor * (0.5 - prob_win_away) * 1

        # Update elos in elo dictionary
        elo_current[home_team] = round(new_home_team_elo, 2)
        elo_current[away_team] = round(new_away_team_elo, 2)

        last_season = current_season

    return elos, elo_probs, elo_current


def __revert_elos_to_mean(current_elos, soft_reset_factor):
    """
    Used to soft reset ELOs when a new seasons data is provided
    """
    elos_mean = np.mean(list(current_elos.values()))

    new_elos_dict = {
        team: (team_elo - elos_mean) * soft_reset_factor + elos_mean for team, team_elo in current_elos.items()
    }

    return new_elos_dict


def apply_historic_elos(features: pd.DataFrame, elos: dict, elo_probs: dict) -> pd.DataFrame:
    """
    Apply values from dictionaries containing historic ELO statistics to dataframe
    """
    features = (features.assign(
        homeElo=lambda df: df.matchID.map(elos).str[0],
        awayElo=lambda df: df.matchID.map(elos).str[1],
        homeEloProb=lambda df: df.matchID.map(elo_probs).str[0],
        awayEloProb=lambda df: df.matchID.map(elo_probs).str[1])
    )

    return features


def apply_current_elos(features: pd.DataFrame, elos_current: dict) -> pd.DataFrame:
    """
        Apply values from dictionary containing current ELO statistics to dataframe
        """
    features = (features.assign(
        homeElo=lambda df: df.homeTeam.map(elos_current),
        awayElo=lambda df: df.awayTeam.map(elos_current))
    )

    features['homeEloProb'] = round(1 / (1 + 10 ** ((features['awayElo'] - features['homeElo']) / 400)), 2)
    features['awayEloProb'] = round(1 - features['homeEloProb'], 2)

    return features


def drop_non_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop columns from provided dataframe
    """
    columns = [
        'matchID',
        'date',
        'round',
        'season',
        'homeTeamID',
        'homeTeam',
        'homeGoals',
        'awayTeamID',
        'awayTeam',
        'awayGoals',
    ]

    df = df.drop(columns, axis=1)

    return df