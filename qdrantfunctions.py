import json
import os

import requests
from phi.vectordb.qdrant import Qdrant
from phi.document import Document


def store_with_embedding(doclist: list[Document]) -> None:
    api_key = os.getenv("QDRANT_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    collection_name = "financial_news"
    vector_db = Qdrant(
        collection=collection_name,
        url=qdrant_url,
        api_key=api_key
    )
    vector_db.insert(documents=doclist)
    print("Added lastest list tweets to qdrant")

def fetch_qdrant() -> Qdrant:
    api_key = os.getenv("QDRANT_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    collection_name = "financial_news"
    vector_db = Qdrant(
        collection=collection_name,
        url=qdrant_url,
        api_key=api_key)
    return vector_db


def fetch_on_topic(topic: str):
    # Qdrant endpoint and API key
    global data
    QDRANT_URL = os.getenv("QDRANT_URL")
    API_KEY = os.getenv("QDRANT_API_KEY")

    # Endpoint and headers
    endpoint = f"{QDRANT_URL}/collections/financial_news/points/scroll"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"  # Authorization header
    }

    # Payload for the POST request
    payload = {
        "limit": 10,
        "filter": {
            "must": [
                {
                    "key": "meta_data.symbol",
                    "match": {
                        "value": topic
                    }
                }
            ]
        }
    }

    try:
        # Perform the POST request
        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))

        # Check the response status
        if response.status_code == 200:
            # Parse and print the response JSON
            data = response.json()
            print("Query successful! Response:")
            # print(json.dumps(data, indent=4))
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")
    return data


# if __name__ == "__main__":
#     detail=fetch_on_topic("ETH")
#     print(detail['result']['points'][0])
