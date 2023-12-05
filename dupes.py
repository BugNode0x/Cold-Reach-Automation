import requests
import json

# Initialize variables
base_url = "https://app.apollo.io/api/v1/emailer_messages/search"
headers = {
        'Content-Length': '217',
        'Content-Type': 'application/json',
        'X-Csrf-Token': 'iJUD1tPIl4ppUISam4fX5oGLY4h4rVqARDrJFOTRsFA7iPOx3tNzmKTx744unepop7ow6LGg9wPuxpMaCSLHaw',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Cookie': 'remember_token_leadgenie_v2=eyJfcmFpbHMiOnsibWVzc2FnZSI6IklqWTBZalZsTldRell6STBaREUzTURCaE0yRTJNREJrTTE5c1pXRmtaMlZ1YVdWamIyOXJhV1ZvWVhOb0lnPT0iLCJleHAiOiIyMDIzLTEyLTA5VDIzOjExOjQyLjkwNVoiLCJwdXIiOiJjb29raWUucmVtZW1iZXJfdG9rZW5fbGVhZGdlbmllX3YyIn19--5ecf86a49c81e2010bece4837b374c73728776a3; iJUD1tPIl4ppUISam4fX5oGLY4h4rVqARDrJFOTRsFA7iPOx3tNzmKTx744unepop7ow6LGg9wPuxpMaCSLHaw; _leadgenie_session=17e5kinSWhqycF2Kw6tVxzVIcKA%2FLxO1YyLlbNup3UhSfVIrwH%2BjM4N2E4Qd%2BAF3MPNim217SjWjjkq4MhA7qj8eUNoCxWiq67ef0AEhiVy07e1JpoYN3KiBOmYN9IeFpIu3bnWrXT48VmW2%2BSlpyshBJ%2FST7tmIzb0kuXFx%2BetYrCJkBLnPzL9tWpltkzUgwlj9PY1weJcdWZLXzfCBO5ioGGZkimWOrpi3RrTVzgkJqYXtmPZ59h3aCEXCtkvmjgwbQL7mw2u6bBysGtjYoW4jyNlsl7Tol44%3D--3oOoBiDmXQ6pn8Qf--0UUk2%2BVrPn0nExvUhOkRjA%3D%3D'
    }
to_name_list = []
duplicates = []

# Function to make POST request
def make_post_request(page):
    payload = {
        "finder_view_id": "5a205be89a57e40c095e1d65",
        "user_ids": ["64b5e5d3c24d1700a3a600d3"],
        "page": page,
        "emailer_message_stats": ["scheduled"],
        "q_keywords": "",
        "display_mode": "explorer_mode",
        "open_factor_names": [],
        "num_fetch_result": 1,
        "show_suggestions": False,
        "ui_finder_random_seed": "p5vfb0zv0k",
        "cacheKey": 1700264221016
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
