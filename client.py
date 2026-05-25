import json
import secrets
import sys
import urllib.error
import urllib.request

P = int(
    "FFFFFFFFFFFFFFFFADF85458A2BB4A9AAFDC5620273D3CF1"
    "D8B9C583CE2D3695A9E13641146433FBCC939DCE249B3EF9"
    "7D2FE363630C75D8F681B202AEC4617AD3DF1ED5D5FD6561"
    "2433F51F5F066ED0856365553DED1AF3B557135E7F57C935"
    "984F0C70E0E68B77E2A689DAF3EFE8721DF158A136ADE735"
    "30ACCA4F483A797ABC0AB182B324FB61D108A94BB2C8E3FB"
    "B96ADAB760D7F4681D4F42A3DE394DF4AE56EDE76372BB19"
    "0B07A7C8EE0A6D709E02FCE1CDF7E2ECC03404CD28342F61"
    "9172FE9CE98583FF8E4F1232EEF28183C3FE3B1B4C6FAD73"
    "3BB5FCBC2EC22005C58EF1837D1683B2C6F34A26C1B2EFFA"
    "886B423861285C97FFFFFFFFFFFFFFFF",
    16,
)
Q = (P - 1) // 2
G = 2
BYTE_LEN = (P.bit_length() + 7) // 8
T_BITS = 256

SERVER_URL = "https://homehub.tail270483.ts.net"


def int_to_hex(n: int, byte_len: int = BYTE_LEN) -> str:
    return n.to_bytes(byte_len, "big").hex()


def hex_to_int(s: str) -> int:
    return int(s, 16)


def _get(path: str) -> tuple[int, dict]:
    try:
        with urllib.request.urlopen(SERVER_URL + path) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "null")


def _post(path: str, body: dict) -> tuple[int, dict]:
    """POST `body` as JSON. Returns (status, body) for all responses; does not raise on 4xx/5xx."""
    req = urllib.request.Request(
        SERVER_URL + path,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read().decode() or "null")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "null")


# Część A: protokół Schnorra

def fetch_and_verify_params() -> None:
    # TODO STUDENT
    raise NotImplementedError


def keygen() -> tuple[int, int]:
    # TODO STUDENT
    raise NotImplementedError


def prover_commit() -> tuple[int, int]:
    # TODO STUDENT
    raise NotImplementedError


def verifier_challenge(t_bits: int = T_BITS) -> int:
    # TODO STUDENT
    raise NotImplementedError


def prover_response(r: int, e: int, x_priv: int) -> int:
    # TODO STUDENT
    raise NotImplementedError


def verifier_check(y: int, a: int, e: int, z: int) -> bool:
    # TODO STUDENT
    raise NotImplementedError


# Część B: klient HTTP

def register(username: str, y: int) -> None:
    # TODO STUDENT: POST /v1/register
    raise NotImplementedError


def login(username: str, x_priv: int) -> str:
    # TODO STUDENT: prover_commit → /login/start → prover_response → /login/finish
    raise NotImplementedError


# Testy lokalne

def test_completeness(n: int = 100) -> None:
    # TODO STUDENT
    raise NotImplementedError


def test_mutation() -> None:
    # TODO STUDENT: z+1 lub a+1 → odrzucenie
    raise NotImplementedError


def test_fake_key() -> None:
    # TODO STUDENT: x' != x_priv → odrzucenie
    raise NotImplementedError


# Demo

def demo(username: str) -> None:
    x_priv, y = keygen()
    register(username, y)
    print(f"[1] zarejestrowano {username}")

    token = login(username, x_priv)
    print(f"[2] zalogowano, token = {token}")

    # TODO STUDENT: krok 3 — login z fałszywym z (z+1) → 401
    raise NotImplementedError


def main() -> int:
    fetch_and_verify_params()
    test_completeness()
    test_mutation()
    test_fake_key()
    demo("TODO_STUDENT@lab")
    return 0


if __name__ == "__main__":
    sys.exit(main())
