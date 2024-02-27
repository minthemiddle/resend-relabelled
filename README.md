# Resend labelled requests

Takes a CSV with human labelled messages.  
If label is a certain type, send message via API.  
  
**Usage**  
Create config: `cp config.json.example config.json`   
`pip install click pandas requests`  

**Test**  
`pip install pytest responses`  
`pytest test_resend_script.py`
