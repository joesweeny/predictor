from predictor.data.calculation import elo


def test_calculate_team_ratings_returns_new_higher_home_rating_and_lower_away_ratings_for_home_win():
    [home, away] = elo.calculate_team_ratings(
        k_factor=25,
        home_team=1567.03,
        away_team=1463.12,
        home_goals=2,
        away_goals=1
    )

    assert home == 1575.9
    assert away == 1454.25


def test_calculate_team_ratings_returns_new_lower_home_rating_and_higher_away_ratings_for_away_win():
    [home, away] = elo.calculate_team_ratings(
        k_factor=25,
        home_team=1567.03,
        away_team=1463.12,
        home_goals=1,
        away_goals=2
    )

    assert home == 1550.9
    assert away == 1479.25


def test_calculate_team_ratings_decreases_home_rating_and_increases_away_rating_for_a_draw_where_home_is_rated_higher():
    [home, away] = elo.calculate_team_ratings(
        k_factor=25,
        home_team=1667.03,
        away_team=1423.12,
        home_goals=1,
        away_goals=1
    )

    assert home == 1659.46
    assert away == 1430.69


def test_calculate_team_ratings_increases_home_rating_and_decreases_away_rating_for_a_draw_where_away_is_rated_higher():
    [home, away] = elo.calculate_team_ratings(
        k_factor=25,
        home_team=1667.03,
        away_team=1723.12,
        home_goals=1,
        away_goals=1
    )

    assert home == 1669.03
    assert away == 1721.12
