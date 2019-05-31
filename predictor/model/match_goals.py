from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
import pandas as pd


def predict_match_goals(features: pd.DataFrame, fixture: pd.DataFrame):
    y = features['over2.5Goals']
    x = features[features.columns[:-1]]

    clf = LogisticRegression(random_state=42)
    clf.fit(x, y)

    proba = clf.predict_proba(fixture)

    prediction1 = {
        'clf': 'LogisticRegression',
        'under': (1 / proba[:, 0]),
        'over': (1 / proba[:, 1])
    }

    clf = LinearDiscriminantAnalysis()
    clf.fit(x, y)

    proba = clf.predict_proba(fixture)

    prediction2 = {
        'clf': 'LinearDiscriminantAnalysis',
        'under': (1 / proba[:, 0]),
        'over': (1 / proba[:, 1])
    }

    clf = GradientBoostingClassifier()
    clf.fit(x, y)

    proba = clf.predict_proba(fixture)

    prediction3 = {
        'clf': 'GradientBoostingClassifier',
        'under': (1 / proba[:, 0]),
        'over': (1 / proba[:, 1])
    }

    return prediction1, prediction2, prediction3
