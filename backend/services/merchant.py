import re

def extract_merchant(description: str) -> str:
    desc = description.lower()

    patterns = {
        "swiggy": "Swiggy",
        "zomato": "Zomato",
        "amazon": "Amazon",
        "uber": "Uber",
        "ola": "Ola",
        "netflix": "Netflix",
        "spotify": "Spotify"
    }

    for key, value in patterns.items():
        if key in desc:
            return value

    # fallback: clean text
    desc = re.sub(r'[^a-zA-Z ]', ' ', desc)
    words = desc.split()

    return words[0].capitalize() if words else "Unknown"
