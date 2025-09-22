import random
import string
from math import gcd

# ---------- Mapping tables ----------
NUM_TO_CHAR = {i + 1: ch for i, ch in enumerate(string.ascii_lowercase)}
NUM_TO_CHAR[27] = " "

# Inverse map, case‑insensitive
CHAR_TO_NUM = {ch: i for i, ch in NUM_TO_CHAR.items()}
CHAR_TO_NUM.update({ch.upper(): i for ch, i in CHAR_TO_NUM.items()})


# ---------- Encoding / Decoding ----------
def encode_to_number(text: str) -> str:
    """
    Encode ``text`` into a single concatenated number string that always
    starts with a leading ``1``.  Two‑digit padding guarantees an
    unambiguous round‑trip.
    """
    parts = []
    for ch in text:
        if ch == " ":
            num = 27
        else:
            num = CHAR_TO_NUM.get(ch)
            if num is None:
                raise ValueError(f"Unsupported character: {repr(ch)}")
        parts.append(f"{num:02d}")  # always two digits
    return "1" + "".join(parts)


def decode_from_number(num_str: str) -> str:
    """
    Decode a number string that begins with a leading ``1`` back to the
    original text.
    """
    if not num_str.startswith("1"):
        raise ValueError("Encoded string must start with a leading '1'.")
    payload = num_str[1:]  # strip the leading 1

    if len(payload) % 2 != 0:
        raise ValueError("Payload length must be even (pairs of digits).")

    chars = []
    for i in range(0, len(payload), 2):
        pair = payload[i : i + 2]
        n = int(pair)
        ch = NUM_TO_CHAR.get(n)
        if ch is None:
            raise ValueError(f"Invalid code {pair} at position {i//2}.")
        chars.append(ch.upper())
    return "".join(chars)


# ---------- Helper: modular inverse ----------
def modinv(a: int, m: int) -> int:
    """Return the modular inverse of a modulo m (a*x ≡ 1 (mod m))."""
    r0, r1 = a, m
    s0, s1 = 1, 0
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    if r0 != 1:  # a and m not coprime
        raise ValueError(f"{a} has no modular inverse modulo {m}")
    return s0 % m


p = 389109764783540066930273125903
q = 271934865632739250640244604831
n = p * q  # modulus
phi = (p - 1) * (q - 1)  # Euler's totient

default_e = 65537
if gcd(default_e, phi) == 1:
    e = default_e
else:
    candidates = [i for i in range(3, phi, 2) if gcd(i, phi) == 1]
    e = random.choice(candidates)

d = modinv(e, phi)  # decryption exponent

public_key = (n, e)
private_key = (n, d)

# ---------- Demo ----------
plain_text = "Hello world"
encoded_str = encode_to_number(plain_text)  # e.g. "11208121227"
print("Encoded string :", encoded_str)

m_int = int(encoded_str)

if m_int >= n:
    raise ValueError(
        f"The integer representation ({m_int}) is larger than the modulus n ({n}). "
        "Pick larger primes or split the message into blocks."
    )

cipher_int = pow(m_int, e, n)
print("Ciphertext (int):", cipher_int)

recovered_int = pow(cipher_int, d, n)
print("Recovered int   :", recovered_int)

recovered_str = str(recovered_int)
if not recovered_str.startswith("1"):
    recovered_str = "1" + recovered_str.zfill(len(encoded_str))

decoded_text = decode_from_number(recovered_str)
print("Decoded text    :", decoded_text)

print("\nSuccess?", decoded_text == plain_text.upper())
