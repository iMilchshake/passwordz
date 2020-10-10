import hashlib
import string
import numpy as np
import win32clipboard

PW_LENGTH = 10
CHARS = string.ascii_lowercase + string.ascii_uppercase + string.digits + "@!_"


def hashSha256(inp: str):
    m = hashlib.sha256()
    m.update(inp.encode('utf-8'))
    return m.digest()


def generatePassword(master_key, password_id):
    inp = master_key + password_id  # concatenate master + pw_id
    hashed = hashSha256(inp)  # hash the input
    pw_full = "".join(list(map(lambda x: CHARS[x], np.array([n for n in hashed]) % len(CHARS))))  # map hash to CHARS
    return pw_full[0:PW_LENGTH]  # cut password off after (PW_LENGTH)


def saveToClipboard(inp: str):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(inp)
    win32clipboard.CloseClipboard()
