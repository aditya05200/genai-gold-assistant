import os
import requests

HARDCODED_GOLD_PRICE = 6000  # INR per gram fallback

def get_gold_price_per_gram():
    """
    Fetch live gold price from GoldAPI.io.
    If API fails, fallback to hardcoded price.
    """
    try:
        api_key = os.getenv("GOLDAPI_KEY")
        if not api_key:
            raise Exception("GoldAPI key missing")

        url = "https://www.goldapi.io/api/XAU/INR"
        headers = {
            "x-access-token": api_key,
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()

        data = response.json()

        # GoldAPI returns price per ounce
        price_per_ounce = data["price"]

        # Convert ounce → gram
        price_per_gram = price_per_ounce / 31.1035

        return round(price_per_gram, 2)

    except Exception:
        # Automatic fallback
        return HARDCODED_GOLD_PRICE
