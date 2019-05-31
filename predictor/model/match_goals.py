from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import pandas as pd


def predict_match_goals(features: pd.DataFrame, fixture: pd.DataFrame) -> dict:
    y = features[features.columns[-1:]]
    x = features[features.columns[:-1]]

    clf = LinearDiscriminantAnalysis()
    clf.fit(x, y)

    proba = clf.predict_proba(fixture)

    prediction = {
        'under': (1 / proba[:, 0]),
        'over': (1 / proba[:, 1])
    }

    return prediction
