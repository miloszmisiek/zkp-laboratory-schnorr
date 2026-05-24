# lab-server

FastAPI service backing **lab 10** of a cryptology course — a live demo of the **interactive Schnorr identification protocol** (zero-knowledge proof of knowledge of a discrete log).

Clients register a public key `y = g^x mod p` over the RFC 7919 **ffdhe2048** group, then prove knowledge of `x` through a three-message commitment / challenge / response flow without ever sending `x`.

All cryptographic primitives are hand-rolled on top of Python `int` and `hashlib`. This is intentional for the lab — no `cryptography` / `pyca` / `pycryptodome`.

## Run

Requires Python 3.10 and [`uv`](https://docs.astral.sh/uv/).

```bash
uv sync
uv run fastapi dev app/main.py     # dev server with reload (default :8000)
uv run fastapi run app/main.py     # production-mode server
```

Interactive API docs: <http://127.0.0.1:8000/docs>.

## Endpoints

| Endpoint              | Method | Purpose                                     |
|-----------------------|--------|---------------------------------------------|
| `/params/`            | GET    | group parameters `(p, q, g)` as padded hex  |
| `/v1/register`        | POST   | register a public key under a username      |
| `/v1/login/start`     | POST   | begin authentication: send commitment `a`   |
| `/v1/login/finish`    | POST   | finish authentication: send response `z`    |

## Layout

```
app/
  crypto.py              group constants, H(), int/hex helpers, in_group()
  schemas.py             Pydantic request/response models with strict hex validation
  state.py               in-memory ServerState (users + sessions) + FastAPI dependency
  main.py                FastAPI app, lifespan, router includes
  routers/
    params.py            GET /params
    v1.py                register, login/start, login/finish
client.py                student-facing reference client (with TODO stubs)
docs/
  Lab_X_skrypt_studencki.md   full lab brief (Polish)
```

## Reference

Full task brief (Polish): [`docs/Lab_X_skrypt_studencki.md`](docs/Lab_X_skrypt_studencki.md).
