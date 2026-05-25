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

## Deploy (Docker + Tailscale Funnel)

The Ubuntu host runs the container with compose and exposes it to the public internet only for the duration of the lab via Tailscale Funnel.

Build / start / stop the container:

```bash
docker compose --profile prod up -d --build    # start (build if needed)
docker compose ps                              # confirm "healthy"
docker compose --profile prod down             # stop
```

Toggle Funnel exposure (modern CLI):

```bash
sudo tailscale funnel --bg 8000           # ON  — exposes container as https://<host>.ts.net
sudo tailscale funnel reset               # OFF — removes all funnel rules
sudo tailscale funnel status              # check what's currently exposed
```

Rate limit is configurable via the `RATE_LIMIT` env var (default `300/minute` per IP via `compose.yaml`; module default in `app/ratelimit.py` is `60/minute`). Override per-deploy with `RATE_LIMIT=... docker compose ...` before `up`.

**Habit:** after every lab, run `sudo tailscale serve status` to confirm Funnel is off. The container can keep running on the tailnet, but nothing should be public outside lab hours.

## Endpoints

| Endpoint              | Method | Purpose                                     |
|-----------------------|--------|---------------------------------------------|
| `/v1/params/`         | GET    | group parameters `(p, q, g)` as padded hex  |
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
    params.py            GET /v1/params
    v1.py                register, login/start, login/finish
client.py                student-facing reference client (with TODO stubs)
docs/
  Lab_X_skrypt_studencki.md   full lab brief (Polish)
```

## Reference

Full task brief (Polish): [`docs/Lab_X_skrypt_studencki.md`](docs/Lab_X_skrypt_studencki.md).
