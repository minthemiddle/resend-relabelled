import pytest
import responses
import json
from resend_script import process_csv, resend_message, API_URL, HUMAN_LABEL

# Assuming config.json is in the same directory as your test file
# If not, adjust the path accordingly
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    API_URL = config['api_url']

# Example of a test function
@responses.activate
def test_resend_message_success():
    responses.add(responses.POST, API_URL, json=[{"is_created": True}], status=200)

    result = resend_message(123)
    assert result['is_created'] is True

@responses.activate
def test_resend_message_failure():
    responses.add(responses.POST, API_URL, json=[{"is_created": False, "reason": "Error"}], status=400)

    result = resend_message(123)
    assert result['is_created'] is False
    assert result['reason'] == "Error"

def test_config_loading():
    """
    Test that the configuration file is loaded correctly and the values are accessible.
    """
    # Load the config file as it is done in the script
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    # Assert that the values match what is expected
    assert API_URL == config['api_url']
    assert HUMAN_LABEL == config['human_label']
