import json
import requests
import os
import sys 
import urllib3
import pytz
import openai
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from urllib.parse import urlparse
from requests.exceptions import HTTPError, ConnectionError


def convert_caps_to_title(name):
    if name.isupper():
        return name.title()
    return name

def clean_organization_name(name):
    # List of common legal entity designations to remove
    legal_suffixes = [
        'LLC', 'Inc', 'Corporation', 'Corp', 'Ltd', 'LP', 'LLP', 'GmbH', 'AG', 'KG', 'Co', 'S.A.', 'NV', 'P.A.', 'CPAs','P.A'
    ]

    # Removing any trailing spaces, commas, or periods
    name = name.strip().rstrip(',')

    # Split the name into parts for easier processing
    name_parts = name.split()
    
    # Remove the legal suffixes and any trailing commas or periods in each part
    cleaned_name_parts = []
    for part in name_parts:
        part = part.rstrip('.').rstrip(',')
        if part not in legal_suffixes:
            cleaned_name_parts.append(part)

    # Reassemble the name, ensuring no trailing commas or spaces
    cleaned_name = ' '.join(cleaned_name_parts).strip().rstrip(',')

    return cleaned_name

def get_utc_datetime_from_est(date_str, time_str='00:00'):
    # Parse the EST datetime
    est_datetime = datetime.strptime(f'{date_str} {time_str}', '%m/%d/%Y %H:%M')
    est = pytz.timezone('America/New_York')
    est_datetime = est.localize(est_datetime)
    
    # Convert to UTC
    utc_datetime = est_datetime.astimezone(pytz.utc)
    return utc_datetime

# Initialize the start time for scheduling emails with date and time in UTC
date_for_scheduling = '12/05/2023'  # Set your desired date here
time_for_scheduling = '17:01'       # Set your desired time here (24-hour format)
current_schedule_time_utc = get_utc_datetime_from_est(date_for_scheduling, time_for_scheduling)

# Initialize the counter for the emails sent within the current hour
emails_sent_this_hour = 0

# Disable SSL warnings (use for debugging only, not recommended for production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set your OpenAI API key (recommended to use environment variable for security reasons)
openai.api_key = ''  # Fallback to a default key

# Specified headers for the requests
headers = {
        'Content-Length': '217',
        'Content-Type': 'application/json',
        'X-Csrf-Token': 'coffee',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Cookie': 'coffee'
    }

# URL for the POST and PUT requests
post_url = 'https://app.apollo.io/api/v1/emailer_messages'

# Read contact IDs from the JSON file
with open('contacts.json', 'r') as file:
    contacts = json.load(file)

# Function to scrape website content
def scrape_website(url):
    return get_website_content(url)  # This calls the new function

def get_website_content(url):
    try:
        # Headers with User-Agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        }

        # Fetching the content of the website with HTTPS, following redirects
        response = requests.get(url, headers=headers, verify=True, allow_redirects=True)

        # Check for 200 OK response
        if response.status_code != 200:
            print(f"URL {url} did not respond with 200 OK. Skipping.")
            return None

        # Parsing the content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Removing script and style elements
        for script_or_style in soup(['script', 'style']):
            script_or_style.extract()

        # Get text and clean it up
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text
    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")
        return None


def preprocess_text(text):
    # Basic preprocessing - select first few sentences
    # Replace this with more advanced logic if needed
    sentences = text.split('.')[:3]  # Get the first three sentences
    return '. '.join(sentences) + '.'

# Function to craft the cold email with a subject and HTML body
def generate_description(text):
    # Adjusted prompt to guide the model
    prompt = (f"Please provide a concise, one-sentence description of the company's product or service, without using quotes, and keeping between 5 to 10 words. This description should fit into the email template: Given the {text}, I thought this might interest you.\n"
              "The company specializes in: {text}\n"
              "Required: A brief, engaging description suitable for a cold email\n"
              "Required: The description should start in lower case and not end with a period.\n"
              "This is the body email logic:\n"
              "Given the (description), I thought this might interest you.\n"
              "Required: Do not use sales vague words such as 'cutting-edge' 'seamless', make it easy to understand")

    # Requesting description from OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "system", "content": "You are an expert in summarizing complex concepts into short, engaging sentences for marketing purposes."},
                  {"role": "user", "content": prompt}]
    )

    # Post-process to remove quotes
    generated_description = response.choices[0].message['content']
    return generated_description.replace('"', '')



# Function to craft the cold email with a subject and HTML body
def craft_email(full_name, organization_name, description):
    # Clean and convert the organization name
    clean_org_name = clean_organization_name(organization_name)
    organization_name = convert_caps_to_title(clean_org_name)

    first_name = full_name.split()[0]
    subject = f"{organization_name} & Red Teaming"

    # Crafting the body text
    body_text = (
        f"{first_name} - We're conversing with cybersecurity professionals to listen to your opinion and feedback on red teaming and tooling.\n\n"
        f"Given your role and the {description} that {organization_name} offers, I thought this might interest you.\n\n"
        f"We're developing a platform for attack surface monitoring, and we'd appreciate your feedback. If interested, do you have 15 minutes next week? I'm open next Monday 1 or 2 pm afternoon EST if it may work for you.\n\n"
        f"Thank you,\n\n"
    )

    # Preparing the description for HTML format
    description_html = description.replace('\n', '<br>')

    # Crafting the HTML version of the email body
    body_html = (
        f"<div>{first_name} - We're conversing with cybersecurity professionals to listen to your opinion and feedback on red teaming and tooling.</div><div><br></div>"
        f"<div>Given your role and the {description_html}  that {organization_name} offers, I thought this might interest you.</div><div><br></div>"
        f"<div>We're developing a platform for attack surface monitoring, and we'd appreciate your feedback. If interested, do you have 15 minutes next week? I'm open next Monday 1 or 2 pm afternoon EST if it may work for you.</div><div><br></div>"
        f"<div>Thank you,</div>"
    )

    return subject, body_text, body_html



# Function to schedule an email
def schedule_email(email_id, schedule_time):
    # Existing PUT request to schedule an email
    put_url = f'https://app.apollo.io/api/v1/emailer_messages/{email_id}'
    put_data = {
        "due_at": schedule_time,
        "surface": "people",
        "cacheKey": 1699903672195
    }
    try:
        put_response = requests.put(put_url, headers=headers, data=json.dumps(put_data), verify=False)
        if put_response.status_code == 200:
            print(f"Email {email_id} scheduled successfully for {schedule_time}")
        else:
            print(f"Failed to schedule email {email_id}: {put_response.text}")
    except Exception as e:
        print(f"An error occurred while scheduling email {email_id}: {e}")

    # New POST request to schedule drafted emails
    post_url = 'https://app.apollo.io/api/v1/emailer_messages/schedule_drafted_emails'
    post_data = {
        "ids": [email_id],
        "surface": "people",
        "cacheKey": 1699114273964
    }
    try:
        post_response = requests.post(post_url, headers=headers, json=post_data, verify=False)
        if post_response.status_code == 200:
            print(f"Drafted email {email_id} scheduled successfully.")
        else:
            print(f"Failed to schedule drafted email {email_id}: {post_response.text}")
    except Exception as e:
        print(f"An error occurred while scheduling drafted email {email_id}: {e}")



# Main execution logic
try:
    total_emails_to_send = 20 * 5   # 20 emails for 5 hours
    email_count = 0

    for contact_index, contact in enumerate(contacts):
        if email_count >= total_emails_to_send:
            break  # Stop if we have scheduled all required emails

        if 'URL' not in contact or not contact['URL']:
            print(f"No URL provided for contact {contact['ID']}. Skipping.")
            continue

        website_content = scrape_website(contact['URL'])
        if website_content is None:
            print(f"Failed to scrape website for contact {contact['ID']}. Skipping.")
            continue

        preprocessed_content = preprocess_text(website_content)
        description = generate_description(website_content)
        subject, body_text, body_html = craft_email(contact['Name'], clean_organization_name(contact['Organization']), description)

        post_data = {
            "contact_id": contact['ID'],
            "subject": subject,
            "body_text": body_text,
            "body_html": body_html
        }

        post_response = requests.post(post_url, headers=headers, data=json.dumps(post_data), verify=False)
        if post_response.status_code == 200:
            response_data = post_response.json()
            email_id = response_data["emailer_message"]["id"]

            schedule_time_str = current_schedule_time_utc.strftime('%Y-%m-%dT%H:%M:%S.000Z')
            schedule_email(email_id, schedule_time_str)
            current_schedule_time_utc += timedelta(minutes=1)

            email_count += 1
            emails_sent_this_hour += 1

            if emails_sent_this_hour >= 20:
                current_schedule_time_utc += timedelta(hours=1) - timedelta(minutes=20)
                emails_sent_this_hour = 0
        else:
            print(f"Failed to post contact {contact['ID']}: {post_response.text}")

except KeyboardInterrupt:
    print('\nProcess was interrupted by user.')
    sys.exit(0)

except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
