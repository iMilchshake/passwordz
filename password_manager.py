import hashlib
import string
import numpy as np


def hash_sha256(inp: str):
    m = hashlib.sha256()
    m.update(inp.encode('utf-8'))
    return m.digest()


def generate_password(master_key, password_id):
    seed = master_key + password_id  # concatenate master + pw_id
    hashed = hash_sha256(seed)  # hash the input
    pw_full = "".join(list(map(lambda x: CHARS[x], np.array([n for n in hashed]) % len(CHARS))))  # map hash to CHARS
    return pw_full[0:PW_LENGTH]  # cut password off after (PW_LENGTH)


if __name__ == "__main__":
    PW_LENGTH = 10
    CHARS = string.ascii_lowercase + string.ascii_uppercase + string.digits + "@!_"
    MASTER = "thisIsAMasterKeyXD"
    password_ids = ('steam', 'reddit', 'twitter', 'twitch')

    for pw_id in password_ids:
        pw = generate_password(MASTER, pw_id)
