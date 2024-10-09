import base64
import requests

# client ID and client secret
client_id = ''
client_secret = ''
account_id = ''

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
    #print(token_info)
    access_token = token_info['access_token']
    print(f"Access Token: {access_token}")
else:
    print(f"Failed to get access token: {response.status_code}")
    print(response.text)

    # Zoom API endpoint for meeting metrics
    metrics_url = 'https://api.zoom.us/v2/metrics/meetings'

    # Headers with the access token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Make the request to the metrics endpoint
    metrics_response = requests.get(metrics_url, headers=headers)

    # Check if the request was successful
    if metrics_response.status_code == 200:
        metrics_info = metrics_response.json()
        print(metrics_info)
    else:
        print(f"Failed to get meeting metrics: {metrics_response.status_code}")
        print(metrics_response.text)
        # Parameters for the metrics request
        params = {
            'from': '2023-01-01',
            'to': '2023-01-31',
            'page_size': '300'
        }

        # Make the request to the metrics endpoint with parameters
        metrics_response = requests.get(metrics_url, headers=headers, params=params)

        # Check if the request was successful
        if metrics_response.status_code == 200:
            metrics_info = metrics_response.json()
            print(metrics_info)
        else:
            print(f"Failed to get meeting metrics: {metrics_response.status_code}")
            print(metrics_response.text)
            # Parameters for the metrics request
            params = {
                'from': '2023-01-01',
                'to': '2023-01-31',
                'page_size': '300'
            }

            # Function to get meeting metrics with pagination
            def get_meeting_metrics(url, headers, params):
                all_metrics = []
                while True:
                    response = requests.get(url, headers=headers, params=params)
                    if response.status_code == 200:
                        data = response.json()
                        all_metrics.extend(data.get('meetings', []))
                        next_page_token = data.get('next_page_token')
                        if not next_page_token:
                            break
                        params['next_page_token'] = next_page_token
                    else:
                        print(f"Failed to get meeting metrics: {response.status_code}")
                        print(response.text)
                        break
                return all_metrics

            # Get all meeting metrics
            all_meeting_metrics = get_meeting_metrics(metrics_url, headers, params)
            print(all_meeting_metrics)
