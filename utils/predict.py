import numpy as np
import pandas as pd
import pickle
import os
from pathlib import Path

from sklearn.model_selection import cross_val_score, RepeatedStratifiedKFold

from utils.transform import resample_data, normalize_data


def transform_fit_predict(X_train, y_train, X_test, y_test,
                          resample, resampling_method,
                          normalize, normalize_method,
                          model,
                          cv_n_splits, cv_n_repeats,
                          method,
                          random_state=None,
                          save_model=False, path=None):
    if resample:
        X_train, y_train = resample_data(X_train, y_train, method=resampling_method, random_state=random_state)

    if normalize:
        X_train, X_test = normalize_data(X_train, X_test, method=normalize_method)

    model.fit(X_train, y_train)
    if save_model:
        if path == None:
            path = Path(os.getcwd())
        with open(path / "trained_model.sav", 'wb') as f:
            pickle.dump(model, f)
        print(f"Trained model saved: {path}")
            
    scores = cross_val_score(model, X_test, y_test, scoring='roc_auc',
                            cv=RepeatedStratifiedKFold(n_splits=cv_n_splits, n_repeats=cv_n_repeats))
    print(f"{method}: {np.mean(scores)}")


def get_rank_predictions(X, y, ranker, target_column,
                         target="data points",
                         top_n=5,
                         round_precision=4):
    results = pd.DataFrame(y)

    pred = ranker.predict(X)
    results['pred_rank'] = pd.Series(pred).rank(method='dense', ascending=True).values
    results['abs_diff'] = abs( results['rank'] - results['pred_rank'] )

    selected_mean_rank = results[results[target_column] <= top_n]['pred_rank'].mean()
    print(f"Mean rank of top {top_n} {target} based on predictions: {round(selected_mean_rank, round_precision)}")
    print(f"Mean rank of all {target} based on predictions: {round(results['pred_rank'].mean(), round_precision)}")
    print(f"Std rank of all {target} based on predictions: {round(results['pred_rank'].std(), round_precision)}")
    print(f"Mean absolute difference between each pair of rank and predicted rank:",
          f"{round(results['abs_diff'].mean(), round_precision)}")
    print(results.sort_values(['pred_rank', target_column]).head(), "\n")
    
    return results.sort_values(['pred_rank', target_column])