# Script made to list contact information from an existing list

import requests
import json

url = "https://app.apollo.io/api/v1/mixed_people/search"
headers = {
        'Content-Length': '217',
        'Content-Type': 'application/json',
        'X-Csrf-Token': 'coffee',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Cookie': 'coffee'
    }

# Initialize the page number
page_number = 1

# Initialize a list to hold all contacts
all_contacts = []

# Loop until an empty 'contacts' list is received
while True:
    # Update the payload with the current page number
    payload = {
        "finder_view_id": "coffee",
        "prospected_by_current_team": ["yes"],
        "page": page_number,
        "contact_label_ids": ["coffee"],
        "display_mode": "explorer_mode",
        "per_page": 25,
        "open_factor_names": [],
        "num_fetch_result": 1,
        "context": "people-index-page",
        "show_suggestions": False,
        "ui_finder_random_seed": "coffee",
        "cacheKey": coffee
    }

    # Send POST request and assign the response to the 'response' variable
    response = requests.post(url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Extract the 'contacts' data
        contacts = data.get('contacts', [])
        
        # Check if the contacts list is empty, which means we've reached the end
        if not contacts:
            print(f"No more contacts found at page {page_number}.")
            break
        
        # Loop through the contacts and save the required information
        for contact in contacts:
            contact_info = {
                "ID": contact.get('id'),
                "Name": contact.get('name'),
                "Title": contact.get('title', 'Not available'),  # Default to 'Not available' if title is not present
                "Organization": contact.get('organization_name'),
                "URL": contact.get('organization', {}).get('website_url', 'Not available')
            }
            # Append the contact info to the all_contacts list
            all_contacts.append(contact_info)
                
        print(f"Page {page_number} processed.")
        page_number += 1
    else:
        print(f"Failed to fetch data at page {page_number}: {response.status_code}")
        break

# Save all contacts to a JSON file
with open('contacts.json', 'w') as json_file:
    json.dump(all_contacts, json_file, indent=4)

print("All pages have been processed. Contact information has been saved to contacts.json")
