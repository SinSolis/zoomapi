import base64
import requests
import json

# Function to get participants for a list of meeting IDs with pagination
def get_meeting_participants(meeting_ids):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    for meeting_id in meeting_ids:
        params = {
            'page_size': '300'
        }
        while True:
            url = f'https://api.zoom.us/v2/metrics/meetings/{meeting_id}/participants'
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                participants = data.get('participants', [])
                print(f"Participants for meeting {meeting_id}:")
                print(json.dumps(participants, indent=4))  # Print the participants in pretty JSON format
                next_page_token = data.get('next_page_token')
                if not next_page_token:
                    break
                params['next_page_token'] = next_page_token
            else:
                print(f"Failed to get participants for meeting {meeting_id}: {response.status_code}")
                break

# Get all meeting metrics and print them
all_meeting_ids = get_meeting_metrics()

# Get participants for all meetings
get_meeting_participants(all_meeting_ids)

# Print the list of all IDs
print(all_meeting_ids)
