import requests
import json
import time
from datetime import datetime

class FlowSender:
    def __init__(self, server_url="http://localhost:5000/upload", token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiU2Vuc29yNCIsImV4cCI6MTczOTk4NjM3MX0.SrS4-JUeO3TY05l-bLowGy2S6BzaH97i6XuwSHZwXj0"):
        self.server_url = server_url
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': token,
            'User-Agent': 'Java/11.0.25',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }

    def extract_json_from_post_data(self, post_data_section):
        # Find the JSON data between the first { and last }
        start_idx = post_data_section.find('{')
        end_idx = post_data_section.rfind('}') + 1
        if start_idx == -1 or end_idx == 0:
            return None
        
        # Extract the JSON string
        json_str = post_data_section[start_idx:end_idx]
        
        # Fix the nested JSON by escaping double quotes
        json_str = json_str.replace('"{', '{').replace('}"', '}')
        json_str = json_str.replace('\\"', '"')  # Unescape any already escaped quotes
        
        return json_str

    def send_flow(self, flow_data):
        try:
            # Parse the flow data string into a dictionary
            flow_dict = json.loads(flow_data)
            
            # Send POST request
            response = requests.post(
                self.server_url,
                headers=self.headers,
                json=flow_dict,
                timeout=5
            )
            
            # Print response details
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return response.status_code == 200
            
        except Exception as e:
            print(f"Error sending flow: {e}")
            return False

def process_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Split the content into individual POST data sections
    sections = content.split('POST Data:')
    
    # Remove the first element (empty or header)
    sections = [s for s in sections if s.strip()]
    
    return sections

if __name__ == "__main__":
    # Initialize the sender
    sender = FlowSender(server_url="http://127.0.0.1:5000/upload", token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiU2Vuc29yNCIsImV4cCI6MTczOTk4NjM3MX0.SrS4-JUeO3TY05l-bLowGy2S6BzaH97i6XuwSHZwXj0")
    
    # Process the file and get POST data sections
    sections = process_file("flask_dash_app/app/sample-post-single.txt")
    
    # Send each flow with a delay
    for i, section in enumerate(sections, 1):
        print(f"\nProcessing flow {i}/{len(sections)}")
        json_data = sender.extract_json_from_post_data(section)
        if json_data:
            print(f"Sending flow at {datetime.now()}")
            success = sender.send_flow(json_data)
            print(f"Send {'successful' if success else 'failed'}")
            time.sleep(1)  # Add delay between requests