import pandas as pd
import numpy as np

from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from sklearn.preprocessing import StandardScaler

import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

from gensim.models.fasttext import FastText


def pivot_data(data, target, binary_target_value=None):
    X_original = data.drop([target], axis=1)
    y_original = data[target]
    y = y_original.apply(lambda x: 1 if x==binary_target_value else 0)

    X = pd.DataFrame()
    for col in X_original.columns:
        if type(X_original[col][0]) == str:
            col_pivoted = pd.get_dummies(X_original[col], prefix=col)
            X = pd.concat([X, col_pivoted], axis=1)
        else:
            X = pd.concat([X, X_original[col]], axis=1)

    return X, y


def resample_data(X_train, y_train, method, random_state=None):
    if method == "upsample":
        X_train_balanced, y_train_balanced = SMOTE(random_state=random_state).fit_resample(X_train, y_train)

    elif method == "downsample":
        X_train_balanced, y_train_balanced = RandomUnderSampler(random_state=random_state).fit_resample(X_train, y_train)
    
    return X_train_balanced, y_train_balanced


def normalize_data(X_train, X_test, method="standard"):
    scaler = StandardScaler()
    X_train_normalized = scaler.fit_transform(X_train)
    X_test_normalized = scaler.transform(X_test)

    return X_train_normalized, X_test_normalized


def numeric_to_interval(data, column, n_intervals):
    col_vals = data[column]
    min_val = np.min(col_vals)
    max_val = np.max(col_vals)
    interval = (max_val - min_val) / n_intervals
    data[column] = pd.cut(col_vals, bins=np.arange(min_val, max_val, interval), right=True)
    
    return data


def concat_counts_df(df1, df1_name, df2, df2_name, column):
    counts_df1 = df1[column].value_counts(sort=False)
    counts_df1.name = f"{df1_name}_{column}"
    counts_df2 = df2[column].value_counts(sort=False)
    counts_df2.name = f"{df2_name}_{column}"
    return pd.concat([
        pd.DataFrame(counts_df1/ sum(counts_df1)).T,
        pd.DataFrame(counts_df2/ sum(counts_df2)).T
        ]).round(2)


def get_numeric_columns(data, cols_to_exclude=None):
    numeric_columns = []
    non_numeric_columns = []
    for col in data.drop(cols_to_exclude, axis=1).columns:
        if type(data[col][0]) == str:
            non_numeric_columns.append(col)
        else:
            numeric_columns.append(col)

    return numeric_columns, non_numeric_columns


def convert_terms(word, convert_terms_dict):
    to_return = word
    for _from, _to in convert_terms_dict.items():
        if word == _from:
            to_return = _to
    
    return to_return


def process_text(text,
                 remove_stopwords=True,
                 lemmatize=True,
                 stem=True):
    
    stop_words = []
    if remove_stopwords:
        stop_words = stopwords.words('english')
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()

    processed = []
    tokens = word_tokenize(text.translate(str.maketrans("", "", string.punctuation)))
    for token in tokens:
        if token not in stop_words:
            if lemmatize:
                lemma = lemmatizer.lemmatize(token)
                if stem:
                    stem = stemmer.stem(token)
                    processed.append(stem)
                else:
                    processed.append(lemma)
            else:
                processed.append(token)
    
    return " ".join(processed)


def convert_words_to_vectors(input_words, reference_vectors, dimension):
    output_vectors = []
    for words in input_words:
        word_vector = np.zeros(dimension)
        for word in words.split():
            try:
                word_vector += reference_vectors[word.lower()]
            except KeyError:
                pass
        
        output_vectors.append(word_vector)

    return np.array(output_vectors)


def get_word_vectors(dataframe, word_col, vectorizer='fasttext',
                     to_process_text=True, remove_stopwords=True, lemmatize=False, stem=False):
    if to_process_text:
        to_convert = dataframe[word_col].apply(
            process_text,
            remove_stopwords=remove_stopwords,
            lemmatize=lemmatize,
            stem=stem
        )
    else:
        to_convert = dataframe[word_col]

    if vectorizer == 'fasttext':
        fasttext = FastText(sentences=to_convert.apply(
            lambda x: [word.lower() for word in x.split()]
            ))
        dimension = fasttext.vector_size
        word_vectors = convert_words_to_vectors(to_convert, fasttext, dimension)

    return word_vectors