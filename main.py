import uuid
from datetime import datetime

from fastapi import FastAPI

app = FastAPI()


@app.get('/', tags=['root'])
async def get_uuid_and_timestamp():
    return f'{datetime.now()}: {uuid.uuid4()}'
