#!/usr/bin/env python
"""
Program to get the WAN IP-address from a DIR-655 router.

Needs a config file named .dir655wanip_config containing one line
format:
  <username>;<password>;<service url>

  username should be admin
  password should be the admin password
  servce url should be the address to the API, http://<router ip>:8099/
"""
import sys
import requests
from bs4 import BeautifulSoup as Soup
from requests.auth import HTTPBasicAuth

CONFIG_FILE = '.dir655wanip_config'

REQUEST_MESSAGE = """
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns:xsd="http://www.w3.org/2001/XMLSchema"
xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
soap:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
<soap:Body>
<GetWanSettings xmlns="http://purenetworks.com/HNAP1/">
</GetWanSettings>
</soap:Body>
</soap:Envelope>
"""


def exit_with_message(message):
  print message
  sys.exit(1)

def read_config():
  # maybe the config file should be a command line arg or env variable
  try:
    with open(CONFIG_FILE, 'r') as config_file:
      config = config_file.readline().strip().split(';')

      if len(config) != 3:
        exit_with_message('config should have <username>;<password>;<service url>')

      if config[0] != 'admin':
        exit_with_message('user name not admin')

      if not config[2].startswith('http'):
        exit_with_message('url to service should start with http')

      return config

  except IOError as e:
    exit_with_message('missing config file: ' + CONFIG_FILE)


def get_ip(config):
  username = config[0]
  password = config[1]
  request_url = config[2]

  resp = requests.post(request_url, auth=HTTPBasicAuth(username, password), data=REQUEST_MESSAGE)
  soup = Soup(resp.text)
  ip_addr = soup.find('ipaddress')

  print ip_addr.contents[0]

  
def main():
 config = read_config()
 get_ip(config)

if __name__ == "__main__":
  main()
