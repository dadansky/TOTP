import time
import hashlib
import uuid
import base58
from typing import Optional


# totp time window in seconds
# would go to a config in a real microservice

time_window = 15


def generate_secret() -> str:
    """Returns a random 20-symbol base58 string"""
    secret_bytes = uuid.uuid4().bytes
    return base58.b58encode(secret_bytes).decode()[:20]


def generate_code(secret: str,
                  seconds_since_the_epoch: Optional[int] = None) -> str:
    """Generates a TOTP code.
    Arguments:
    secret -- 20-symbol base58 string to act as a secret key to make TOTP code
    seconds_since_the_epoch -- second for which to generate. Current moment if None

    Returns 4-digit string that changes every window"""

    if len(secret) > 20:
        raise ValueError("Secret must be 20-symbol base58 string, is '{}' instead".format(secret))

    if seconds_since_the_epoch is None:
        seconds_since_the_epoch = int(time.time())
    seconds_since_the_epoch = int(seconds_since_the_epoch // time_window)

    code = str(seconds_since_the_epoch)

    hash = hashlib.sha256(code.encode()).hexdigest()

    b58 = base58.b58decode_int(base58.b58encode(hash))

    return str(b58)[-4:]


def check_code(secret: str, code: str,
               seconds_since_the_epoch: Optional[int] = None) -> bool:
    """Checks if the code is correct for the current moment.
    Arguments:
    secret -- 20-symbol base58 string to act as a secret key to generate TOTP code
    code -- 4-digit string TOTP code.
    seconds_since_the_epoch -- moment at which code should be correct

    Returns True if the code is valid for the provided moment
    """
    if len(code) != 4:
        raise ValueError("TOTP code must be 4 digits string, is '{}' instead".format(code))
    return generate_code(secret, seconds_since_the_epoch) == code
