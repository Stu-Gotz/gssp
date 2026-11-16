import re
import unicodedata


def to_id(name):
    """Bridge to assist mapping Showdown to PokeAPI."""
    if not name:
        return ""
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", ascii_name.lower())
