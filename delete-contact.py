import requests
import json
import urllib3

# Suppress only the single InsecureRequestWarning from urllib3 needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to make the POST request and return the contact IDs
def get_contact_ids(page):
    url = "https://app.apollo.io/api/v1/emailer_messages/search"
    payload = {
        "finder_view_id": "5a205be89a57e40c095e1d65",
        "page": page,
        "display_mode": "explorer_mode",
        "open_factor_names": [],
        "num_fetch_result": 1,
        "show_suggestions": False,
        "ui_finder_random_seed": "6n9tguk444g",
        "cacheKey": 1699233816503
    }

    headers = {
        'Content-Length': '217',
        'Content-Type': 'application/json',
        'X-Csrf-Token': 'iJUD1tPIl4ppUISam4fX5oGLY4h4rVqARDrJFOTRsFA7iPOx3tNzmKTx744unepop7ow6LGg9wPuxpMaCSLHaw',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Cookie': 'remember_token_leadgenie_v2=eyJfcmFpbHMiOnsibWVzc2FnZSI6IklqWTBZalZsTldRell6STBaREUzTURCaE0yRTJNREJrTTE5c1pXRmtaMlZ1YVdWamIyOXJhV1ZvWVhOb0lnPT0iLCJleHAiOiIyMDIzLTEyLTA5VDIzOjExOjQyLjkwNVoiLCJwdXIiOiJjb29raWUucmVtZW1iZXJfdG9rZW5fbGVhZGdlbmllX3YyIn19--5ecf86a49c81e2010bece4837b374c73728776a3; iJUD1tPIl4ppUISam4fX5oGLY4h4rVqARDrJFOTRsFA7iPOx3tNzmKTx744unepop7ow6LGg9wPuxpMaCSLHaw; _leadgenie_session=17e5kinSWhqycF2Kw6tVxzVIcKA%2FLxO1YyLlbNup3UhSfVIrwH%2BjM4N2E4Qd%2BAF3MPNim217SjWjjkq4MhA7qj8eUNoCxWiq67ef0AEhiVy07e1JpoYN3KiBOmYN9IeFpIu3bnWrXT48VmW2%2BSlpyshBJ%2FST7tmIzb0kuXFx%2BetYrCJkBLnPzL9tWpltkzUgwlj9PY1weJcdWZLXzfCBO5ioGGZkimWOrpi3RrTVzgkJqYXtmPZ59h3aCEXCtkvmjgwbQL7mw2u6bBysGtjYoW4jyNlsl7Tol44%3D--3oOoBiDmXQ6pn8Qf--0UUk2%2BVrPn0nExvUhOkRjA%3D%3D'
    }

    # Disable SSL certificate verification
    response = requests.post(url, headers=headers, json=payload, verify=False)
    if response.status_code == 200:
        return response.json().get('emailer_messages', [])
    else:
        print(f"Failed to retrieve data for page {page}: {response.status_code}")
        return None

# Function to delete contacts from the local JSON file
def delete_contacts_from_json(contact_ids_set, json_file_path):
    # Read the existing contacts from the JSON file
    with open(json_file_path, 'r') as file:
        contacts = json.load(file)

    # Filter out contacts whose ID is in the contact_ids_set
    contacts = [contact for contact in contacts if contact["ID"] not in contact_ids_set]

    # Write the updated contacts back to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(contacts, file, indent=4)

# Main loop to iterate over all pages
all_contact_ids = set()
current_page = 1

while True:
    emailer_messages = get_contact_ids(current_page)
    if not emailer_messages:  # If no messages are returned, we've reached the last page
        break

    for message in emailer_messages:
        contact_id = message.get('contact_id')
        if contact_id:
            all_contact_ids.add(contact_id)

    current_page += 1  # Go to the next page

# Now that we have all unique contact IDs, we can delete them from the JSON file
delete_contacts_from_json(all_contact_ids, 'contacts.json')

# Print all unique contact IDs
for contact_id in all_contact_ids:
    print(contact_id)
