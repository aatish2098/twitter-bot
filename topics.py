from typing import List, Dict, Any

import requests


# Define the URL
def get_trending() -> list[dict[str, Any]]:
    url = "https://api.coingecko.com/api/v3/search/trending"

    # Send GET request
    response = requests.get(url, headers={"accept": "application/json"})

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Initialize an empty list to store the extracted coin data
        topics = []

        # Loop through the coins in the response
        for coin in data.get("coins", []):
            item = coin.get("item", {})
            # Extract the required fields
            coin_data = {
                "symbol": item.get("symbol"),
                "name": item.get("name"),
                "market_cap_rank": item.get("market_cap_rank"),
                "coin_price_usd": item.get("data", {}).get("price"),
                "market_cap": item.get("data", {}).get("market_cap"),
            }
            # Append the extracted data to the topics list
            topics.append(coin_data)
        return topics
