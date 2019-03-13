# fortivpngen
A script that creates vpn tunnels on fortios firewalls.
It is important to understand that this script ist created to use with a automation tool like
puppet, chef  

A yaml config file for constants
 
generated key length
Certificate location certificates must be same name with tunnel and a .crt 

phase1 encryption details
tunnel mode Aggressive/Main
ike Version 1/2
DPD status boolean
Xauth status boolean


phase2 encryption details

It has 3 switches 
- create
- delete
- list


## create
Takes parameters necessary for creating phase1 and phase2 tunnel. Based on tunnel type you
    the ingested parameters vary. here are 2 simple examples
   
   ###if it is route based
   it will automatically create static routes with prefix on config.yml
   
    fortivpngen.py --create vpntunnelname fw_Out_interface remotegateway source_subnet dest_subnet
       
   ###if it is selector based
   it will automatically create 
   - static routes with prefix on config.yml
   - firewall rules with prefix on config.yml
   
    fortivpngen.py --create --selector vpntunnelname fw_Out_interface remotegateway source_subnet dest_subnet
       
## list
    Lists created vpn tunnels 
    --status
        show a vpn tunnel statistic on console

## delete
    deletes a tunnel 
    --name name to delete tunnel
    fortivpngen --delete -my_first_tunnel 



