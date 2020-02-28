import requests
from dotenv import load_dotenv
import os

load_dotenv()

bearer =  os.environ.get('bearer-token')
url = "https://api.assetpanda.com:443//v2/entities/100780/objects"

# for each loop iterates through dict
payload = {'field_8': 'OptiPlex 7050',
'field_6': 'Dell Inc.',
'field_138': 'PPM-MIS1',
'field_10': '8CZ1TM2',
'field_134': 'PPM Info Technology Svcs-8291-10022',
'field_135': 'ADMINISTRATION & FINANCE',
'field_155': '00:0E:C6:B1:F0:D8',
'field_154': '130.166.8.60'}
files = [   

]
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Authorization' : 'Bearer {}'.format(bearer)
}

response = requests.request("POST", url, headers=headers, data = payload, files = files)
if(response.status_code == 422):
    """
    run update asset
    """

print(response.status_code)
