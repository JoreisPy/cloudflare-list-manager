import argparse
import configparser
import json
import requests
import os

# Get the path of the current script
script_path = os.path.dirname(os.path.abspath(__file__))

# Read the Cloudflare account information from the config file
config = configparser.ConfigParser()
config.read(f'/{script_path}/credentials.cfg')
cf_email = config.get('cloudflare', 'email')
cf_api_key = config.get('cloudflare', 'api_key')
account_id = config.get('cloudflare', 'account_id')
list_id = config.get('cloudflare', 'list_id')

# Define the base URL for Cloudflare API requests
base_url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/rules/lists'
headers = {
  'X-Auth-Email': cf_email,
  'X-Auth-Key':   cf_api_key,
  'Content-Type': 'application/json',
  'Cookie': '__cflb=0H28vgHxwvgAQtjUGU56Rb8iNWZVUvXhincQSARpxUu; __cfruid=371a7e0b3c2684cefeb9b3eb20c1559c5e3e9fa1-1676797492'
}

# Returns all items from the list
def get_all_items_from_lits(list_id):
        response = requests.request("GET", f'{base_url}/{list_id}/items', headers=headers)
        ips = response.json()['result']
        return ips

# Returns an item ID proving an IP
def get_item_id(ip_or_sub):
    IPs = get_all_items_from_lits(list_id)
    for items in IPs:
        if items["ip"] == ip_or_sub:
            return items["id"]

# Define a function to get the contents of the allowed_ips list
def get_list(list_id):
    try:
        response = requests.request("GET", f'{base_url}/{list_id}/items', headers=headers)
        if response.status_code == 200:
            ips = response.json()['result']
            ips_fornated = json.dumps(ips, indent=4)
            print(f'Contents of allowed_ips: {ips_fornated}')
            return ips
        else:
            print(f'Error getting contents of {list_id}: {response.text}')
    except requests.exceptions.RequestException as e:
        print(f'Error getting contents of {list_id}: {e}')



# Define a function to add an IP or subnet to the allowed_ips list
def add_ip(list_id, ip, comment):
    try:
        payload = [
            {
    "ip": ip,
    "comment": comment
            }
        ]

        #data = json.dumps(data)
        response = requests.request("POST", f'{base_url}/{list_id}/items', headers=headers, json=payload)

        if response.status_code == 200:
            print(f'Added {ip} to the {list_id} list')
        else:
            print(f'Error adding {ip} to the {list_id} list: {response.text}')
    except requests.exceptions.RequestException as e:
        print(f'Error adding {ip} to the {list_id} list: {e}')

# Define a function to remove an IP or subnet from the allowed_ips list
def delete_ip(list_id, ip):
    try:
        payload = {"items":[{"id":get_item_id(ip)}]}
        response = requests.request("DELETE", f'{base_url}/{list_id}/items', headers=headers, json=payload)

        if response.status_code == 200:
            print(f'Removed {ip} from the {list_id} list')
        else:
            print(f'Error removing {ip} from the {list_id} list: {response.text}')
    except requests.exceptions.RequestException as e:
        print(f'Error removing {ip} from the {list_id} list: {e}')

# Parse the command line arguments
parser = argparse.ArgumentParser(description='Manage Cloudflare IP lists')
parser.add_argument('--list', action='store_true', help='Lists the contents of the List. No argument needed.')
parser.add_argument('--add', type=str, nargs=2, metavar=("IP", "COMMENT"), help="Add an IP address or subnet to the rule")
parser.add_argument('--delete', type=str, help='the IP or subnet to remove from the list')
args = parser.parse_args()
# Handle the command line arguments
if args.list:
    get_list(list_id)
elif args.add:
    add_ip(list_id, args.add[0], args.add[1])
elif args.delete:
    delete_ip(list_id, args.delete)
else:
    parser.print_help()

