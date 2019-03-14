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
   
   ### if it is route based
   it will automatically create static routes with prefix on config.yml
   
    fortivpngen.py --create vpntunnelname fw_Out_interface remotegateway source_subnet dest_subnet
    fortivpngen.py -C new_tunnel_2 wan1 5.4.3.2 192.168.0.0/24 192.168.10.0/24
       
   ### if it is selector based
   It is on todo list but what it is going to do basically is ;
   automatically create 
   - static routes with prefix and a random 4 digit number on config.yml
   - firewall rules with prefix and a random 4 digit number on config.yml
   
    fortivpngen.py --create selector vpntunnelname fw_Out_interface remotegateway source_subnet dest_subnet
       
## list
   Lists created vpn tunnels, it is created for debugging purposses
   -L, --list
   show a vpn tunnel statistic on console
   
       fortivpngen.py --list 
       fortivpngen.py -L 
   
   Sample output
    
       C:\Python37\python.exe C:/fortivpngen/fortivpngen.py --list 
       connection to Fortigate established
       'new_tunnel_2' 5.4.3.2:0  selectors(total,up): 1/0  rx(pkt,err): 0/0  tx(pkt,err): 0/0
       'Datacenter' 185.141.110.220:0  selectors(total,up): 0/0  rx(pkt,err): 0/0  tx(pkt,err): 0/4
        Process finished with exit code 0



## delete
   deletes a tunnel 
    --name name to delete tunnel
    
    fortivpngen --delete my_first_tunnel 



