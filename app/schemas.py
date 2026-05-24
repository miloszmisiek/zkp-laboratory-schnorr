from pydantic import BaseModel, StringConstraints
from typing import Annotated

Hex128   = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{32}$")]
Hex256   = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{64}$")]
Hex2048  = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{512}$")]
Username = Annotated[str, StringConstraints(min_length=1, max_length=64, strip_whitespace=True)]


class RegisterRequest(BaseModel):
    username: Username
    public_key: Hex2048


class LoginStartRequest(BaseModel):
    username: Username
    a: Hex2048


class LoginStartResponse(BaseModel):
    session_id: Hex128
    e: Hex256


class LoginFinishRequest(BaseModel):
    session_id: Hex128
    z: Hex2048


class LoginFinishResponse(BaseModel):
    token: Hex128
