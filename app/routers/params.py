from fastapi import APIRouter

from app.crypto import BYTE_LEN, G, P, Q, int_to_hex

router = APIRouter(prefix="/v1/params", tags=["v1"])


@router.get("/")
def get_params():
    return {
        "p": int_to_hex(P),
        "q": int_to_hex(Q),
        "g": int_to_hex(G),
        "byte_len": BYTE_LEN,
    }
