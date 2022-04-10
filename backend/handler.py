import sys
sys.path.insert(0, 'src/vendor')
import json
import joblib
import pandas as pd
from sqlalchemy import create_engine

import env

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Credentials': True,
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
    "Access-Control-Allow-Headers": "X-Requested-With, content-type, Authorization"
}

def hello(event, context):
    try:
        import unzip_requirements
    except ImportError:
        pass
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    headers = {**HEADERS, **{
        "Content-Type": "application/json"
    }}

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": headers
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """


def test_connection(event, context):
    try:
        import unzip_requirements
    except ImportError:
        pass
    engine = create_engine('postgresql://{user}:{pw}@{host}:{port}/{dbname}'.
                           format(user=env.user, pw=env.password, host=env.host, port=5432,
                                  dbname=env.database))
    headers = {**HEADERS, **{
        "Content-Type": "text/html"
    }}
    if engine:
        response = {
            "statusCode": 200,
            "body": "<html><body><p>Connection Successful</p></body></html>",
            "headers": headers
        }
        return response
    else:
        response = {
            "statusCode": 500,
            "body": "<html><body><p>Could not establish connection</p></body></html>",
            "headers": headers
        }
        return response


def get_data(event, context):
    try:
        import unzip_requirements
        import joblib
    except ImportError:
        pass
    headers = {**HEADERS, **{
        "Content-Type": "application/json"
    }}
    try:
        engine = create_engine('postgresql://{user}:{pw}@{host}:{port}/{dbname}'.
                               format(user=env.user, pw=env.password, host=env.host, port=5432,
                                      dbname=env.database))
        df = pd.read_sql_table('squirrels', engine)

        if not df.empty:
            data = df.to_dict(orient='records')
            response = {
                "statusCode": 200,
                "body": json.dumps(data),
                "headers": headers
            }
            return response
        else:
            response = {
                "statusCode": 500,
                "body": json.dumps({"error": "Could not read database"}),
                "headers": headers
            }
            return response
    except Exception as e:
        response = {
            "statusCode": 500,
            "body": json.dumps({"error": f"{str(e)}"}),
            "headers": headers
        }
        return response


def predict(event, context):
    flags = event["queryStringParameters"]['flags']
    twitches = event["queryStringParameters"]['twitches']
    primary_fur_color = event["queryStringParameters"]['primary_fur_color']
    model = joblib.load(f'model.pkl')
    X = pd.DataFrame({
        'Tail flags': [flags],
        'Tail twitches': [twitches],
        'Primary Fur Color': [primary_fur_color],
    })
    p = model.predict(X)
    return p[0]


if __name__ == "__main__":
    # res = test_connection(None, None)
    # print(res)
    # res = get_data(None, None)
    pass
