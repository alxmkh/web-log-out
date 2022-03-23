import json
import uuid
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import requests

import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title='web-log-output-app')
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get('/lo-get-data-from-file', tags=['get data from ping-pong app'])
async def get_timestamp_and_ping_pong_counter_from_file() -> str:
    try:
        data = f'{datetime.now()}: {uuid.uuid4()}'
        with open(os.getenv("MOUNT"), 'r', encoding='utf-8') as fr:
            data_from_ping_pong_file = fr.read()
        return data + ', ' + data_from_ping_pong_file
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))


@app.get('/lo-get-data-from-rest', tags=['get data from ping-pong app'])
async def get_timestamp_and_ping_pong_counter_from_rest() -> dict:
    try:

        data_from_ping_pong_rest = requests.get(os.getenv("BASE_PING_PONG_URL") + 'pp-get-data-from-rest')
        result = {
            "Message": os.getenv("MESSAGE"),
            datetime.now(): uuid.uuid4(),
            'Ping / Pongs:': json.loads(data_from_ping_pong_rest.content.decode('utf-8'))['pong']
        }
        return result
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))


@app.get('/health-check-pp-app')
async def get_check_pp_app():
    result = requests.get(os.getenv("BASE_PING_PONG_URL") + 'health-app')
    if 200 <= result.status_code <= 303:
        return {"check_pp_app": "OK"}
    else:
        return {"check_pp_app": "FAIL"}
