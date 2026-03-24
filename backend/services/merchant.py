import re

def extract_merchant(description) -> str:
    desc = str(description).lower()

    # Handle UPI patterns
    if "upi" in desc:
        parts = desc.split("/")
        if len(parts) > 1:
            possible = parts[-1]
            if possible.isalpha() and len(possible) > 3:
                return possible.capitalize()
        return "UPI"

    patterns = {
        "swiggy": "Swiggy",
        "zomato": "Zomato",
        "amazon": "Amazon",
        "uber": "Uber",
        "ola": "Ola",
        "netflix": "Netflix",
        "spotify": "Spotify",
        "fuel": "Fuel",
        "gas": "Fuel",
        "petrol": "Fuel",
        "atm": "ATM"
    }

    for key, value in patterns.items():
        if key in desc:
            return value

    desc = re.sub(r'[^a-zA-Z ]', ' ', desc)
    words = desc.split()

    return words[0].capitalize() if words else "Unknown"