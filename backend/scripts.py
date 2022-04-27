import pandas as pd
import joblib
from sqlalchemy import create_engine
from sklearn import preprocessing as pre
from sklearn import linear_model
from sklearn import svm
from sklearn.tree import DecisionTreeRegressor
import sklearn.model_selection as select
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.feature_selection import f_classif, mutual_info_classif, SelectFromModel

import env

engine = create_engine('postgresql://{user}:{pw}@{host}:{port}/{dbname}'.
                       format(user=env.user, pw=env.password, host=env.host, port=5432,
                              dbname=env.database))


def get_conn():
    conn = psycopg2.connect(
        dbname=env.database,
        user=env.user,
        password=env.password,
        port=5432,
        host=env.host
    )
    conn.autocommit = True
    return conn


def populate_table(local_path: str, table_name: str):
    df = pd.read_csv(local_path)
    engine = create_engine(f'postgresql+psycopg2://{env.user}:{env.password}@{env.host}:5432/{env.database}')
    # df.to_sql(table_name, engine, if_exists='replace', method='multi', index=False)
    return df


def get_data() -> pd.DataFrame:
    data = pd.read_sql_table('squirrels', engine)
    # data.drop([], inplace=True, axis=1)
    return data


def split_data(X, y, ):
    test_size = 0.15
    X_train, X_test, y_train, y_test = select.train_test_split(X, y, test_size=test_size, random_state=69)

    return X_train, X_test, y_train, y_test


def preprocess_data(categorical_cols: list, numeric_cols: list):
    numerical_transformer = SimpleImputer(strategy='median')
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numeric_cols),
            ('cat', categorical_transformer, categorical_cols)
        ])

    return preprocessor


def make_model(df):
    feature_cols = ['Tail flags','Tail twitches', 'Primary Fur Color', 'Approaches']
    categorical_feature_cols = ['Primary Fur Color']
    numeric_feature_cols = ['Tail flags','Tail twitches']
    df = df[feature_cols]
    df.drop_duplicates(subset=['Unique Squirrel ID'], inplace=True)
    df.dropna(inplace=True)
    y = df['Approaches']
    X = df[categorical_feature_cols + numeric_feature_cols]
    X_train, X_valid, y_train, y_valid = split_data(X, y)

    preprocessor = preprocess_data(categorical_feature_cols, numeric_feature_cols)

    model = svm.LinearSVC()

    model_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                     # ('scaler', pre.StandardScaler(with_std=False, with_mean=False)),
                                     ('model', model)
                                     ])

    model_pipeline.fit(X_train, y_train)
    preds = model_pipeline.predict(X_valid)
    scores=model_pipeline.score(X_valid,preds)
    print('=====================================================')
    print(scores)

    joblib.dump(model_pipeline, f'model.pkl')


def main():
    # df = populate_table('/Users/jared.stock/Downloads/2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv',
    #                     'squirrels')
    df = get_data()
    make_model(df)


def test(flags, twitches, primary_fur_color):
    model = joblib.load(f'model.pkl')
    X = pd.DataFrame({
        'Tail flags': [flags],
        'Tail twitches': [twitches],
        'Primary Fur Color': [primary_fur_color],
    })
    p = model.predict(X)
    print(p)


if __name__ == '__main__':
    main()
    test(True, True, 'Gray')
