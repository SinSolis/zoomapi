import base64
import requests
import json

def get_access_token(client_id, client_secret, account_id):

    # Encode client ID and client secret in base64
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    # Zoom OAuth token endpoint
    token_url = 'https://zoom.us/oauth/token'

    # Request parameters
    params = {
        'grant_type': 'account_credentials',
        'account_id': account_id,
    }

    # Headers with encoded credentials
    headers = {
        'Authorization': f'Basic {encoded_credentials}'
    }

    # Make the request
    response = requests.post(token_url, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        token_info = response.json()
        return token_info['access_token']
    else:
        print(f"Failed to get access token: {response.status_code}")
        #print(response.text)
        return None

# Get access token
access_token = get_access_token(client_id, client_secret, account_id)

# Function to get meeting metrics with pagination
def get_meeting_metrics():
    url = 'https://api.zoom.us/v2/metrics/meetings'  # Define the metrics URL
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    params = {
        'from': '2024-10-09 00:01:10',
        'to': '2024-10-09 00:01:20',
        'page_size': '300'
    }

    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            meetings = data.get('meetings', [])
            print(json.dumps(meetings, indent=4))  # Print the metrics in pretty JSON format
            next_page_token = data.get('next_page_token')
            if not next_page_token:
                break
            params['next_page_token'] = next_page_token
        else:
            print(f"Failed to get meeting metrics: {response.status_code}")
            break

# Get all meeting metrics and print them
get_meeting_metrics()
