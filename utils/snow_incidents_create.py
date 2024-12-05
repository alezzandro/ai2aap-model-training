#!/bin/python3
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os
import sys

def create_servicenow_incident(instance_url, username, password, description, host):
    """Creates a new incident in ServiceNow with the given description.

    Args:
        instance_url (str): Your ServiceNow instance URL (e.g., "https://yourinstance.service-now.com")
        username (str): Your ServiceNow username
        password (str): Your ServiceNow password
        description (str): The description of the incident
        host: The host to troubleshoot

    Returns:
        dict: The response from ServiceNow, including the sys_id of the new incident if successful.
    """

    url = f"{instance_url}/api/now/table/incident"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    s = requests.Session()
    retries = Retry(total=5, connect=5, read=5, redirect=5, backoff_factor=2)
    s.mount('https://', HTTPAdapter(max_retries=retries))
    # Payload with incident details
    data = {
        "short_description": description,
        "u_host": host
    }
    try:
        response = s.response = requests.post(url, auth=(username, password), headers=headers, json=data)
    except Exception as e:
        print(f"Error: received exception connecting to the SNow instance {instance_url}")
        print(e)
        return None

    if response.status_code == 201:
        result = response.json()
        sys_id = result['result']['sys_id']  # Extract sys_id if creation successful
        print(f"Incident created successfully with sys_id: {sys_id}")
        return result
    else:
        print(f"Error creating incident: {response.status_code} - {response.text}")
        return None  # Return None on failure
    


# Example Usage:
instance_url = os.environ.get('SNOW_URL', "https://YOUR_INSTANCE.service-now.com")
username = os.environ.get('SNOW_USER', "alejandro.mascall")
password = os.environ.get("SNOW_PASSWORD", 'your password)')
incidents = [
        {"description": "Database performance is degraded in the test environment, maybe it's a network congestion or storage latency, please investigate", "node": "node2"},
        {"description": "Virtual machine 'develop15' failing due to insufficient disk space. Please do cleanup or archival actions or evaluate storage expansion options.", "node": "node3"}, 
        {"description": "Website performance is significantly degraded after upgrade, please rollback to the previous version and investigate the issue.", "node": "node1"}
    ]

def usage():
    print("Usage: %s [predefined|custom]" % sys.argv[0])
    exit(255)

if len(sys.argv) != 2:
    usage()

if sys.argv[1] == "predefined":
    print("Creating predefined incidents")
    for inc in incidents:
        print("Creating incident:")
        print(f"Node: {inc['node']}")
        print(f"Description: {inc['description']}")
        response_data = create_servicenow_incident(instance_url, username, password, inc["description"], inc["node"])
elif sys.argv[1] == "custom":
    print("Creating custom incidents")
    try:
        while True:
            print("Press CTRL-D to exit")
            node = input("Enter the node affected by the incident: ")
            description = input("Enter the incident description: ")
            response_data = create_servicenow_incident(instance_url, username, password, description, node)
    except:
        pass
else:
    usage()
    #if response_data is not None:
    #    # Optionally, process the response data
    #    print("Response Data:", response_data)

