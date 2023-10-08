import openai
from notion.client import NotionClient
import yagmail

import requests
import openai
import yagmail

# Set up constants
NOTION_TOKEN = "secret_KrgWxFgv5t2T4tTCyNugmCamJviHctRlJne7BPo99WM"
NOTION_DATABASE_ID = "399a9fcb196e4b1faa2e536a7d5d1840"
OPENAI_API_KEY = "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"
EMAIL = "netfaithconnection@gmail.com"
EMAIL_PASSWORD = "wtyztjskcejnddhx"

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

# Set up Notion headers
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2021-08-16",  # This might need updating in the future
    "Content-Type": "application/json"
}

# Connect to your Notion database
def get_notion_data(database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    response = requests.post(url, headers=HEADERS, json={})
    return response.json().get("results", [])


email_users = [user for user in get_notion_data(NOTION_DATABASE_ID) if user["properties"]["Communication"]["select"]["name"] == "Email"]

yag = yagmail.SMTP(EMAIL, EMAIL_PASSWORD)

def send_email(recipient, subject, content):
    yag.send(
        to=recipient,
        subject=subject,
        contents=content
    )

# ...
for user in email_users:
    name = user["properties"]["Name"]["title"][0]["text"]["content"]
    interest = user["properties"]["Interest Topics"]["select"]["name"]
    email_address = user["properties"]["Email"]["email"]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Given a note from a faith leader about {interest}, generate a concise and straightforward paragraph that provides spiritual insight and guidance on the topic, tailored for individuals interested in {interest}. The content should resonate with {name} and be easily understandable, avoiding complex jargon. Focus on delivering a clear message that aligns with the theme of the note and addresses the specific interests of the individual."},
        ]
    )

    blog_content = response.choices[0].message["content"].strip()  # Use 'message' and 'content' here

    send_email(email_address, f"Spiritual Guidance on {interest}", blog_content)
# ...










