import numpy as np
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