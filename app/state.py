from dataclasses import dataclass, field
from fastapi import Request

@dataclass
class Session:
    username: str
    a: int
    e: int


@dataclass
class ServerState:
    users: dict[str, int] = field(default_factory=dict)
    sessions: dict[str, Session] = field(default_factory=dict)


def get_state(request: Request) -> ServerState:
    return request.app.state.server_state
