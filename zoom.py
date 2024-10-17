def get_meeting_participants(meeting_ids):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    all_participants = []  # Initialize an empty list to store all participants
    
    for meeting_id in meeting_ids:
        params = {
            'page_size': '300',
            'type': 'past'
        }
        while True:
            url = f'https://api.zoom.us/v2/metrics/meetings/{meeting_id}/participants'
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                participants = data.get('participants', [])
                for participant in participants:
                    participant['meeting_id'] = meeting_id  # Add meeting_id to each participant
                    # Add prefix to each field
                    for key in list(participant.keys()):
                        participant[f'participant_{key}'] = participant.pop(key)
                all_participants.extend(participants)  # Add participants to the all_participants list
                next_page_token = data.get('next_page_token')
                if not next_page_token:
                    break
                params['next_page_token'] = next_page_token
            else:
                print(f"Failed to get participants for meeting {meeting_id}: {response.status_code}")
                break
    
    return all_participants  # Return the list of all participants
