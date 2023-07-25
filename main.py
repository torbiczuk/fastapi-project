import asyncio

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis import Redis

import auth.router
import microwave.router
import websocket.router
from websocket.router import broadcast_status

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router.router, tags=["Authentication"])
app.include_router(microwave.router.router, prefix="/microwave", tags=["Microwave"])
app.include_router(websocket.router.router, prefix="/ws", tags=["Websocket"])


def create_websocket_broadcast_task():
    redis_client = Redis(host='localhost', port=6379, db=0)
    loop = asyncio.get_event_loop()
    loop.create_task(broadcast_status(redis_client))


create_websocket_broadcast_task()
