import requests

def check_stock(product_id, store_ids):
    """
    Sends a POST request to the Boots API to check stock levels for a product in multiple stores.

    Args:
        product_id (str): The product ID to check stock for.
        store_ids (list): A list of store IDs to query.

    Returns:
        dict: The response data from the API.
    """
    url = "https://www.boots.com/online/psc/itemStock"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    payload = {
        "productIdList": [product_id],
        "storeIdList": store_ids
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return None


def parse_stock_levels(response_data, store_id_map):
    """
    Parses the stock levels from the API response and maps store IDs to names.

    Args:
        response_data (dict): The API response containing stock levels.
        store_id_map (dict): A dictionary mapping store IDs to their names.

    Returns:
        list: A list of dictionaries with store names and stock statuses.
    """
    results = []
    stock_mapping = {
        "R": "Out of Stock",
        "G": "In Stock",
        "A": "Limited Stock"
    }

    for stock_info in response_data.get("stockLevels", []):
        store_id = stock_info.get("storeId")
        stock_level = stock_mapping.get(stock_info.get("stockLevel", ""), "Unknown Status")
        store_name = store_id_map.get(store_id, f"Store ID {store_id}")

        results.append({
            "store_name": store_name,
            "stock_status": stock_level
        })

    return results


# Define product ID and store IDs
product_id = "11464911000001101"  # Replace with the desired product ID
store_ids = [723, 1111, 1156, 877, 1521, 1533, 2178, 951, 2173, 2197]  # Replace with desired store IDs

# Map store IDs to human-readable names
store_id_map = {
    "723": "Boots Oxford Street",
    "1111": "Boots Piccadilly Circus",
    "1156": "Boots Marble Arch",
    "877": "Boots Liverpool Street",
    "1521": "Boots Paddington",
    "1533": "Boots King's Cross",
    "2178": "Boots Canary Wharf",
    "951": "Boots Camden",
    "2173": "Boots Notting Hill",
    "2197": "Boots Waterloo"
}

# Check stock
response_data = check_stock(product_id, store_ids)

# Parse and display results
if response_data:
    stock_results = parse_stock_levels(response_data, store_id_map)

    print("Stock Information:")
    for result in stock_results:
        print(f"Store: {result['store_name']}, Stock Status: {result['stock_status']}")
else:
    print("No response or failed to retrieve stock information.")
