import click
from numpy.core.multiarray import empty
import pandas as pd
import requests
import json
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the config.json file
config_path = os.path.join(script_dir, 'config.json')

# Read the configuration file
with open(config_path, 'r') as config_file:
    config = json.load(config_file)
    API_URL = config['api_url']
    HUMAN_LABEL = config['human_label']


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output_file', type=click.Path(), default=None)
def process_csv(input_file, output_file):
    """
    Process the CSV file to resend messages based on the given conditions and update the CSV accordingly.
    """
    df = pd.read_csv(input_file)
    
    # Check if 'status_resend' column exists, if not, create it with default values as None
    if 'resend_status' not in df.columns:
        df['resend_status'] = None
    
    df['resend_fail_reason'] = None

    for index, row in df.iterrows():
                
        if row['resend_status'] in ['success', 'fail']:
            continue

        if row.get('classification_human') == HUMAN_LABEL:
            # print(f"Considered: {row['resend_status']}, {row['resend_fail_reason']}, Message: {row['message'][:10]}") 
            # continue
            response = resend_message(row['id'])
            if response and response.get('is_created'):
                df.at[index, 'resend_status'] = 'success'
            else:
                df.at[index, 'resend_status'] = 'fail'
                df.at[index, 'resend_fail_reason'] = response.get('reason') if response else 'No response from API'

    output = output_file or input_file
    df.to_csv(output, index=False)
    click.echo(f"Processed file saved as: {output}")

def resend_message(contact_form_id):
    """
    Send a POST request to the API to resend the message with the given contact_form_id.
    """
    headers = {'Content-Type': 'application/json'}
    data = json.dumps([
        {
            "contact_form_id": contact_form_id,
            "message_type": "REQUEST_FOR_INFORMATION"
        }
    ])

    try:
        response = requests.post(API_URL, headers=headers, data=data)
        return response.json()[0]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    process_csv()
