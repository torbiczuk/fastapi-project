import asyncio
from auth.dependencies import validate_websocket_jwt_token
from fastapi import APIRouter, Depends, WebSocket, HTTPException
from redis import Redis

from websocket.schemas import MicrowaveState, ClientMessage

router = APIRouter()
WEBSOCKETS_OPEN = set()

# TODO add tests
# TODO use aioredis to make async endpoints
redis_client = Redis(host='localhost', port=6379, db=0)  # TODO move to config


def get_redis_client():
    return redis_client


def get_microwave_state(redis: Redis = Depends(get_redis_client)) -> MicrowaveState:
    state_data = redis.get("microwave_state")
    if state_data:
        return MicrowaveState.model_validate_json(state_data)
    else:
        return MicrowaveState()


def validate_microwave_state(state: MicrowaveState):
    pass


def update_microwave_state(state: MicrowaveState):
    redis = get_redis_client()
    redis.set("microwave_state", state.model_dump_json())
    return state


async def broadcast_status(redis):
    while True:
        await asyncio.sleep(1)  # Wait for 1 seconds
        state = get_microwave_state(redis)
        # Send the current status to all connected clients
        for websocket in WEBSOCKETS_OPEN:
            await websocket.send_text(state.model_dump_json())
            print('send')
            print()


@router.websocket("/microwave/{token}")
@router.websocket("/microwave/")
async def websocket_endpoint(websocket: WebSocket, redis: Redis = Depends(get_redis_client)):
    await websocket.accept()
    WEBSOCKETS_OPEN.add(websocket)
    # Start the status update broadcasting in the background
    while True:
        state = get_microwave_state(redis)
        await websocket.send_text(state.model_dump_json())

        # receive from client
        message = await websocket.receive_text()
        clean_data = ClientMessage.model_validate_json(message)
        if clean_data.action == 'cancel':
            try:
                validate_websocket_jwt_token(clean_data.access_token)
                print(clean_data.access_token)
            except HTTPException:
                print('Invalid token')
                continue
            new_state = MicrowaveState()
        else:
            print(message)
            new_state = MicrowaveState.model_validate_json(message)
        print(new_state)
        update_microwave_state(new_state)
