# Cloudflare IP List Management

This project is a command line tool for managing IP lists in Cloudflare. It allows you to add, delete, and list IP addresses or subnets in a specific IP list on your Cloudflare account. You can use this tool to easily manage your Cloudflare IP lists without having to log into the Cloudflare web interface.

## Installation

1. Clone the repository
2. Create a virtual environment:
```shell
python -m venv env
```
3. Activate the virtual environment:
- Windows: `.\env\Scripts\activate`
- Linux/macOS: `source env/bin/activate`
4. Install the required packages:

```shell
pip install -r requirements.txt
```

## Configuration

To use this tool, you need to create a `credentials.cfg` file with your Cloudflare credentials. The `credentials.cfg` file should be in the following format:

#### [cloudflare]
- email = your-email@example.com
- api_key = your-global-api-key
- account_id = Your account ID
- list_id = Your List ID, considering that Cloudflare allows only 1 list in the free tier, I am not bothering to make this dinamic. But can be easily changed.

An example is provided in the root directory of the project.
```shell
cp credentials.cfg.example credentials.cfg
```

#### how to get Accound ID and List ID:

1. Log in to your Cloudflare account.
2. Navigate to the "Manage Account" section of the Cloudflare dashboard.
3. Click on the "Confiugurations tab.
4. Under "Lists", click on "Create a List" to create a new list, or click on an existing list to view its details.
5. Look at the URL in your web browser's address bar. The account ID is located after the dash.cloudflare.com/ path and before the /firewall/rules/lists/ path. The list ID is located after the rules/lists/ path. Please use this URL for referrence:  https://dash.cloudflare.com/<`account_id`>/firewall/rules/lists/<`list_id`>/.


## Usage

To use this tool, run the `cf_ip_list.py` script with the appropriate command line arguments. Here are the available commands:

- `--list : List the contents of the IP list with the specified `list_id`.
- `--add <ip_or_subnet> <Comment>`: Add the specified `ip_or_subnet` to the IP list with the specified `list_id`.
- `--delete <ip_or_subnet>`: Remove the specified `ip_or_subnet` from the IP list with the specified `list_id`.
- `--help`: Show the usage instructions.

replace `<ip_or_subnet>` with the IP address or subnet you want to add or remove.

Here are some examples of how to use this tool:

 - List the contents of the "allowed_ips" list
```shell
python cf_ip_list.py --list
```
- Add the IP address "192.168.0.1" to the "allowed_ips" list
```shell
python cf_ip_list.py --add  192.168.0.1 'This is an Example
```

- Remove the subnet "192.168.0.0/24" from the "allowed_ips" list
```shell
python cf_ip_list.py --delete  192.168.0.0/24
```