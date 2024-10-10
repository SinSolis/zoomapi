import base64
import requests
import json

# Function to get meeting metrics with pagination
def get_meeting_metrics():
    url = 'https://api.zoom.us/v2/metrics/meetings'  # Define the metrics URL
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    params = {
        'type': 'past',
        'from': '2024-10-09 00:01:10',
        'to': '2024-10-09 00:01:20',
        'page_size': '300'
    }

    all_ids = []
    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            meetings = data.get('meetings', [])
            print(json.dumps(meetings, indent=4))  # Print the metrics in pretty JSON format
            for meeting in meetings:
                all_ids.append(meeting.get('id'))
            next_page_token = data.get('next_page_token')
            if not next_page_token:
                break
            params['next_page_token'] = next_page_token
        else:
            print(f"Failed to get meeting metrics: {response.status_code}")
            break
    return all_ids

# Get all meeting metrics and print them
all_meeting_ids = get_meeting_metrics()

# Print the list of all IDs
print(all_meeting_ids)
