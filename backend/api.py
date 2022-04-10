import json
import joblib
import pandas as pd
from sqlalchemy import create_engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import env

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:19006",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/hello/")
async def hello():
    return {'hello': 'world'}


@app.get("/predict/")
async def predict(flags: str, twitches: str, primary_fur_color: str):
    model = joblib.load(f'model.pkl')
    X = pd.DataFrame({
        'Tail flags': [flags],
        'Tail twitches': [twitches],
        'Primary Fur Color': [primary_fur_color],
    })
    p = list(model.predict(X))
    pred = p[0]
    return {"prediction": bool(pred)}


@app.get("/squirrels/")
async def get_squirrels():
    engine = create_engine('postgresql://{user}:{pw}@{host}:{port}/{dbname}'.
                           format(user=env.user, pw=env.password, host=env.host, port=5432,
                                  dbname=env.database))
    print('GET SQUIRRELS')
    feature_cols = ['Shift', 'Age', 'Primary Fur Color', 'Location', 'Tail flags','Tail twitches', 'Approaches', 'Unique Squirrel ID']

    df = pd.read_sql_table('squirrels', engine)
    df=df[feature_cols]
    df.drop_duplicates(subset=['Unique Squirrel ID'],inplace=True)
    df.dropna(inplace=True)

    # print(df['Primary Fur Color'].unique())

    if not df.empty:
        data = df.head(25).to_dict(orient='records')
        print('RETURN')
        return data
    else:
        return 'GET ERROR'
