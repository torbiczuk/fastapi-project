from fastapi import APIRouter, HTTPException, Depends
from redis import Redis

from auth.dependencies import get_current_user
from auth.schemas import SystemUser
from microwave.schemas import MicrowaveState, PowerRequest, CounterRequest

router = APIRouter()

# TODO add tests
# TODO use aioredis to make async endpoints
redis_client = Redis(host='localhost', port=6379, db=0)  # TODO move to config


def get_redis_client():
    return redis_client


def get_microwave_state(redis: Redis = Depends(get_redis_client)):
    state_data = redis.get("microwave_state")
    if state_data:
        return MicrowaveState.model_validate_json(state_data)
    else:
        return MicrowaveState()


def update_microwave_state(state: MicrowaveState):
    redis = get_redis_client()
    redis.set("microwave_state", state.model_dump_json())
    return state


@router.get("/", response_model=MicrowaveState)
async def get_microwave(state: MicrowaveState = Depends(get_microwave_state)):
    return state


@router.post("/power/", response_model=MicrowaveState)
def power_level(request: PowerRequest, microwave_state: MicrowaveState = Depends(get_microwave_state)):
    if request.power > 0 and microwave_state.power >= 250:
        raise HTTPException(status_code=400, detail="Too much power")
    else:
        new_value = microwave_state.power + request.power
        if new_value <= 0:
            microwave_state.power += request.power
            microwave_state.on = False
        else:
            microwave_state.power = new_value
            microwave_state.on = True
        update_microwave_state(microwave_state)
        return microwave_state


@router.post("/counter/", response_model=MicrowaveState)
def counter(request: CounterRequest, microwave_state: MicrowaveState = Depends(get_microwave_state)):
    new_value = microwave_state.counter + request.counter
    if new_value <= 0:
        microwave_state.counter = 0
        microwave_state.on = False
    else:
        microwave_state.counter = new_value
        microwave_state.on = True
    update_microwave_state(microwave_state)
    return microwave_state


@router.put("/cancel/", response_model=MicrowaveState)
def cancel(user: SystemUser = Depends(get_current_user)):
    state = MicrowaveState()
    return update_microwave_state(state)

