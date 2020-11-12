from typing import List
from compiler.grpc.proto.event_pb2 import CardEvent, GoalEvent


def calculate_adjusted_goals(team_id: int, home: bool, goals: List[GoalEvent], cards: List[CardEvent]) -> float:
    team_goals = []
    red_cards = []

    for goal in goals:
        if goal.team_id == team_id:
            team_goals.append(goal)

    for card in cards:
        if (card.team_id != team_id) and (card.type == 'redcard'):
            red_cards.append(card)

    if (len(red_cards) == 0) and (len(team_goals) <= 2):
        return len(team_goals)

    return __calculate_goals_total(home, team_goals, red_cards)


def __calculate_goals_total(home: bool, goals: List[GoalEvent], cards: List[CardEvent]) -> float:
    total = 0

    for goal in goals:
        if goal.minute <= 60 or total <= 1:
            if __goal_before_red_card(goal, cards):
                total += 1
            else:
                total += 0.5
        else:
            if __goal_before_red_card(goal, cards):
                total += __calculate_goal_value(home, goal)
            else:
                total += __calculate_goal_value(home, goal) / 2

    return total


def __calculate_goal_value(home: bool, goal: GoalEvent) -> float:
    score = goal.score.split('-')

    if home:
        difference = int(score[0]) - int(score[1])
    else:
        difference = int(score[1]) - int(score[0])

    if difference <= 1:
        return 1

    return 0.5


def __goal_before_red_card(goal: GoalEvent, cards: List[CardEvent]) -> bool:
    if len(cards) == 0:
        return True

    for card in cards:
        if goal.minute < card.minute:
            return True

    return False
