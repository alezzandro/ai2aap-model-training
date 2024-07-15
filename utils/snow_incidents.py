#!/opt/app-root/bin/python

import requests

def get_servicenow_incidents(instance_url, username, password):
    """Fetches incidents from a ServiceNow instance using REST API.

    Args:
        instance_url (str): Your ServiceNow instance URL (e.g., https://yourinstance.service-now.com)
        username (str): Your ServiceNow username
        password (str): Your ServiceNow password

    Returns:
        list: A list of dictionaries, each representing an incident.
    """
    
    url = f"{instance_url}/api/now/table/incident"
    headers = {"Accept": "application/json"}  # Specify JSON response

    response = requests.get(url, auth=(username, password), headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("result", [])  # Extract incident list or empty list if not found
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []  # Return empty list in case of errors

# Example usage
instance_url = "https://dev243595.service-now.com"
username = "Incident.Manager"
password = "***"

incidents = get_servicenow_incidents(instance_url, username, password)

# Process the incidents (e.g., print details)
for incident in incidents:
    if incident['state'] == "1": 
        print(f"Number: {incident['number']}, Description: {incident['description']}") 
