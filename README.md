dir655wanip
===========

Get the IP-address from a D-link DIR-655 router and post via ftp to a server.

Uses a HNAP1 interface to get the IP-address of the WAN port.


Configuration
=============

The dir655wanip.py program expects a file called .dir655wanip_config in the working dir with the format:
  username;password;service url
  
  where username should be admin
        password the DIR-655 admin password
        service url http://<router internal ip>:8099/
        
The update_ftp.py program expects a file called .ftp_config in the working dir with the format:
  username;password;ftp address;remote dir
  