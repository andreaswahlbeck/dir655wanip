#!/usr/bin/env python
"""
Program to put the ip-address of router WAN interface on ftp server
"""

import dir655wanip as du
import os.path
from ftplib import FTP

FTP_CONFIG_FILE = '.ftp_config'
IP_ADDRESS_TEMP_FILE = '.current_wan_ip'

def read_ftp_config(ftp_config_file = FTP_CONFIG_FILE):
  try:
    with open(ftp_config_file, 'r') as config_file:
      config = config_file.readline().strip().split(';')

      if len(config) != 4:
        du.exit_with_message('config should have <username>;<password>;<ftp address>;<remote dir>')

      return config

  except IOError as e:
    du.exit_with_message('missing config file: ' + cf)

def ip_address_updated(ip_address):
  if os.path.isfile(IP_ADDRESS_TEMP_FILE):
    with open(IP_ADDRESS_TEMP_FILE,'r') as old_ip_file:
      old_ip = old_ip_file.readline().strip()
      if old_ip == ip_address:
        return False

  with open(IP_ADDRESS_TEMP_FILE, 'w') as ip_temp_file:
    ip_temp_file.write(ip_address + '\n')

  return True


def put_file_on_ftp(ftp_config):
  print 'updating ftp'
  with open(IP_ADDRESS_TEMP_FILE, 'r') as ip_address_file:
    ftp = FTP(ftp_config[2])
    ftp.login(ftp_config[0],ftp_config[1])
    ftp.cwd(ftp_config[3])
    ftp.storlines("STOR index.html", ip_address_file)
    ftp.quit()


def get_router_ip():
  router_config = du.read_router_config()
  ip_address = du.get_router_wan_ip(router_config)
  return ip_address

def main():
  ip_address = get_router_ip()
  if ip_address_updated(ip_address):
    ftp_config = read_ftp_config()
    put_file_on_ftp(ftp_config)

if __name__ == "__main__":
  main()
