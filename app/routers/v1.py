import secrets

from fastapi import APIRouter, Depends, HTTPException
from app.schemas import (
    LoginFinishRequest,
    LoginFinishResponse,
    LoginStartRequest,
    LoginStartResponse,
    RegisterRequest,
)
from app.state import Session, get_state
from app.crypto import CHALLENGE_BYTES, G, P, Q, hex_to_int, in_group, int_to_hex

router = APIRouter(prefix="/v1", tags=["v1"])


@router.post("/register", status_code=201)
async def register(req: RegisterRequest, state=Depends(get_state)) -> None:
    y = hex_to_int(req.public_key)

    if not in_group(y):
        raise HTTPException(status_code=400, detail="Public key is not a valid group element")

    if pow(y, Q, P) != 1:
        raise HTTPException(status_code=400, detail="Public key is not in prime-order subgroup")

    if req.username in state.users:
        raise HTTPException(status_code=409, detail="Username already taken")

    state.users[req.username] = y


@router.post("/login/start", status_code=200)
async def login_start(req: LoginStartRequest, state=Depends(get_state)) -> LoginStartResponse:
    if req.username not in state.users:
        raise HTTPException(status_code=404, detail="User not found")

    a = hex_to_int(req.a)

    if not in_group(a):
        raise HTTPException(status_code=400, detail="a is not a valid group element")

    if pow(a, Q, P) != 1:
        raise HTTPException(status_code=400, detail="a is not in prime-order subgroup")

    e = secrets.randbits(256)
    session_id = secrets.token_hex(16)

    state.sessions[session_id] = Session(username=req.username, a=a, e=e)

    return LoginStartResponse(session_id=session_id, e=int_to_hex(e, CHALLENGE_BYTES))


@router.post("/login/finish", status_code=200)
async def login_finish(req: LoginFinishRequest, state=Depends(get_state)) -> LoginFinishResponse:
    session = state.sessions.pop(req.session_id, None)
    if session is None:
        raise HTTPException(status_code=401, detail="Session not found or already used")

    y = state.users.get(session.username)
    if y is None:
        raise HTTPException(status_code=401, detail="User no longer exists")

    z = hex_to_int(req.z)
    if not 0 <= z < Q:
        raise HTTPException(status_code=401, detail="z out of range")

    lhs = pow(G, z, P)
    rhs = (session.a * pow(y, session.e, P)) % P
    if lhs != rhs:
        raise HTTPException(status_code=401, detail="Proof verification failed")

    token = secrets.token_hex(16)
    return LoginFinishResponse(token=token)
