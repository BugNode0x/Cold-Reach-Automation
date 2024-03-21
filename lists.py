# Script made to list contact information from an existing list

import requests
import json

url = "https://app.apollo.io/api/v1/mixed_people/search"
headers = {
        'Content-Length': '217',
        'Content-Type': 'application/json',
        'X-Csrf-Token': 'IHfgdAuJ8hkKZSoJPDpimGyTQvHPLgGomVVqytn3TrA02hN6R5lEFQULcxPmMDjVIvbvVUbHOYdaPApaGNO5Fg',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Cookie': 'amplitude_id_122a93c7d9753d2fe678deffe8fac4cfapollo.io=eyJkZXZpY2VJZCI6IjE5MTllMTEyLWZkMmYtNDFiOS05YTRlLWU5NmM0OWNiYmNjYVIiLCJ1c2VySWQiOiI2NWZjOGU0MGE2NjRkOTAyZTg2ZmU2ZTQiLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE3MTEwNTAwOTc2MTAsImxhc3RFdmVudFRpbWUiOjE3MTEwNTMzODg5NDYsImV2ZW50SWQiOjY4LCJpZGVudGlmeUlkIjoyMiwic2VxdWVuY2VOdW1iZXIiOjkwfQ==; intercom-device-id-dyws6i9m=d4d87ebb-06b2-44f6-a922-d53eb3dec4b0; intercom-session-dyws6i9m=TS84SG9vWVZoSlZoVWh3ZWt4TFM5ZEJIakwxYlZRUFlQZHpBVEZsUEZ0T01SQmg0dXA2YW9mczJOc0FselF6bC0ta3JiRm9jWEc5clcxM21RUnZuZldzUT09--7a1e9a46a969062276bc01f478466793ba6651cd; __stripe_mid=fe43c6f3-ea6a-4835-bcad-d51fe70d47061a864e; __stripe_sid=ca679523-8906-4a7f-b798-cb16ff6ab98847bc5b; X-CSRF-TOKEN=IHfgdAuJ8hkKZSoJPDpimGyTQvHPLgGomVVqytn3TrA02hN6R5lEFQULcxPmMDjVIvbvVUbHOYdaPApaGNO5Fg; _leadgenie_session=jWEftszrzJsJNklZkpX%2Fgoz%2BJmHPKut0wBJ5%2BRI0x8PkGLgQMsxQJuvGZbcDixEWPAppanSGsus90rMGA8pxYLOiXqoL3EuBYkOuItXg%2BT45JEBiLN48iwasW7sCas%2BsMZC22e9J045Kh%2F1WAk%2FheSSF%2FTCud4unDrSOijFi3L76AzHtnSNvjXTOTa0g412fLsFgybv%2FE%2FaAiQLual2fjKdDFgj1xXGxdhBqx%2FWRz%2F5%2FL%2BQYIvEAgEgjjtIAj8SzzrZk6dBgHORWE8WJDt%2FNn0U59Q3y9dPpaqk%3D--yGitNIbRzhR5k4zC--aneLvJi7pvu2UGL5AEoIYQ%3D%3D; _clsk=cxiy4l%7C1711053387065%7C6%7C1%7Cl.clarity.ms%2Fcollect; __hssc=21978340.8.1711050338236; __hssrc=1; __hstc=21978340.eda4177bc17b4679bdd56a7ff0da8868.1711050338236.1711050338236.1711050338236.1; hubspotutk=eda4177bc17b4679bdd56a7ff0da8868; _dd_s=rum=0&expire=1711054285601; GCLB=CNqV18zooYvuXRAD; remember_token_leadgenie_v2=eyJfcmFpbHMiOnsibWVzc2FnZSI6IklqWTFabU00WlRRd1lUWTJOR1E1TURKbE9EWm1aVFpsTkY4NVpqZG1PRGhpT0dNNVpEZGhZVFJsTldNelpXWmtOVE5rT1daak5EWm1OeUk9IiwiZXhwIjoiMjAyNC0wNC0yMVQyMDoxNzoyOS4zMDVaIiwicHVyIjoiY29va2llLnJlbWVtYmVyX3Rva2VuX2xlYWRnZW5pZV92MiJ9fQ%3D%3D--44b88926f5e2652421a826e622a2f28c6461b7ab; __q_state_xnwV464CUjypYUw2=eyJ1dWlkIjoiMjMyZTBkZjItZjE4YS00ZmNkLWJiNjItOGM0NWZhNjkyNTI1IiwiY29va2llRG9tYWluIjoiYXBvbGxvLmlvIn0=; _ga_76XXTC73SP=GS1.1.1711050418.1.1.1711052243.60.0.1331408289; _gcl_au=1.1.1135988011.1711052244; mutiny.user.session_number=1; zp__initial_utm_medium=(none); zp__initial_utm_source=(direct); zp__utm_medium=(none); zp__utm_source=(direct); mutiny.user.session=36600c8c-718c-4ef7-9bc7-54776ef7853f; mutiny.user.token=445a41fe-77f3-44f1-b134-2853a3f0ec47; _fbp=fb.1.1711050292398.1684500544; _ga=GA1.1.729939845.1711050418; _cioid=65fc8e40a664d902e86fe6e4; ZP_LATEST_LOGIN_PRICING_VARIANT=23Q4_EC_Z59; ZP_Pricing_Split_Test_Variant=23Q4_EC_Z59; _cioanonid=77e34bbe-18dc-2fa7-d6ff-e5dc62b2dce5; _clck=8jc5la%7C2%7Cfk9%7C0%7C1541; ps_mode=trackingV1'
    }

# Initialize the page number
page_number = 1

# Initialize a list to hold all contacts
all_contacts = []

# Loop until an empty 'contacts' list is received
while True:
    # Update the payload with the current page number
    payload = {
        "finder_view_id": "65fc9bd6e5e9310439728b8c",
        "prospected_by_current_team": ["yes"],
        "page": page_number,
        "contact_label_ids": ["65fc97ee6199af02e799e071"],
        "display_mode": "explorer_mode",
        "per_page": 25,
        "open_factor_names": [],
        "num_fetch_result": 1,
        "context": "people-index-page",
        "show_suggestions": False,
        "ui_finder_random_seed": "stw6fzc5vd",
        "cacheKey": 1699133122321
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
