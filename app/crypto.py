# RFC 7919 ffdhe2048 — p is a 2048-bit safe prime.
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

# Sophie Germain prime: q = (p - 1) / 2.
Q = (P - 1) // 2

G = 2

# Byte length of a group element.
BYTE_LEN = (P.bit_length() + 7) // 8

# Byte length of the challenge e (t = 256 bits).
CHALLENGE_BYTES = 32

def int_to_hex(n: int, byte_len: int = BYTE_LEN) -> str:
    """Encode int as lowercase hex, zero-padded to byte_len bytes."""
    if n < 0:
        raise ValueError("negative integers are not valid group elements")
    return n.to_bytes(byte_len, "big").hex()

def hex_to_int(s: str) -> int:
    """
    Decode lowercase hex (no '0x' prefix) to int.
    Raises ValueError on malformed input.
    """
    if not isinstance(s, str) or not s:
        raise ValueError("expected non-empty hex string")
    try:
        return int(s, 16)
    except ValueError as e:
        raise ValueError(f"not a valid hex string: {e}") from e


def in_group(n: int) -> bool:
    """Check n in Z*_p (1 < n < p)."""
    return 1 < n < P
