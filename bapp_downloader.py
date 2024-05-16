import requests
import os
import re
import argparse
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def sanitize_filename(filename):
    return re.sub(r'[\\/:*?"<>|]', '_', filename)

parser = argparse.ArgumentParser(description='Baixar plugins do BurpSuite.')
parser.add_argument('--proxy', type=str, help='O proxy a ser usado.')
args = parser.parse_args()

url = "https://portswigger.net/bappstore"

proxies = {}
if args.proxy:
    proxies = {
        'http': args.proxy,
        'https': args.proxy,
    }

response = requests.get(url, proxies=proxies, verify=False)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    extension_links = soup.find_all('a', class_='bapp-label')

    for link in extension_links:
        extension_name = link.text
        extension_hash = link['href'].split('/')[-1]

        download_url = f"https://portswigger-cdn.net/bappstore/bapps/download/{extension_hash}"

        os.makedirs('bapps', exist_ok=True)

        sanitized_extension_name = sanitize_filename(extension_name)
        file_path = os.path.join('bapps', f"{sanitized_extension_name}.bapp")

        response = requests.get(download_url, proxies=proxies, verify=False)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloading '{extension_name}'...")
        else:
            print(f"[!] Failed to download '{extension_name}'.")
