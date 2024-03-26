import requests
import json

# Initialize variables
base_url = "https://app.apollo.io/api/v1/emailer_messages/search"
headers = {
        'Content-Length': '217',
        'Content-Type': 'application/json',
        'X-Csrf-Token': 'coffee',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Cookie': 'coffee'
    }
to_name_list = []
duplicates = []

# Function to make POST request
def make_post_request(page):
    payload = {
        "finder_view_id": "coffee",
        "user_ids": ["coffee"],
        "page": page,
        "emailer_message_stats": ["scheduled"],
        "q_keywords": "",
        "display_mode": "explorer_mode",
        "open_factor_names": [],
        "num_fetch_result": 1,
        "show_suggestions": False,
        "ui_finder_random_seed": "coffee",
        "cacheKey": coffee
    }

    response = requests.post(base_url, headers=headers, data=json.dumps(payload))
    try:
        return response.json()
    except json.JSONDecodeError:
        print("Failed to parse JSON. Response content:", response.content)
        return None

# Function to check for duplicates
def check_duplicates(names):
    unique_names = set()
    duplicates = []
    for name in names:
        if name in unique_names:
            duplicates.append(name)
        else:
            unique_names.add(name)
    return duplicates

# Main loop to iterate over pages
page = 1
while True:
    response_data = make_post_request(page)
    if response_data is None or not response_data.get('emailer_messages'):  # Adjusted check here
        break

    # Extract 'to_name' from each item in 'emailer_messages'
    to_name_list.extend([item.get('to_name') for item in response_data['emailer_messages'] if item.get('to_name')])
    page += 1

# Check for duplicates
duplicates = check_duplicates(to_name_list)

# Output the result
print("Duplicated names:", duplicates)
