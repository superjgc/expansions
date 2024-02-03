import re


def to_camel(key: str, cap=False):
    sub_key = key.split("_")
    key = sub_key[0] + "".join([k.capitalize() for k in sub_key[1:]])
    if cap:
        key = "".join([k.capitalize() for k in sub_key])
    return key


def to_underline(key: str):
    return re.sub(r"[A-Z]", lambda match: f"_{match.group(0).lower()}", key).strip("_")
