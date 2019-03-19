# fortivpngen
A script that creates vpn tunnels on fortios firewalls.
It is important to understand that this script ist created to use with a automation tool like
puppet, chef  

It connects to firewall using an ssh user and pushes cli scripts for necessary configurations

[![IMAGE ALT TEXT](http://img.youtube.com/vi/nr1l1f048QI/0.jpg)](http://www.youtube.com/watch?v=nr1l1f048QI "Watch in action")

A yaml config file for constants
 
generated key length that specified in yaml file
 

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

## config.yml file explained
Ipsec vpn tunnels are constructed on 2 phases first one makes sure of peers
second one deals with key exchange and encryption of data details.

As usual using the latest encryption methods are  always prefered.
At some cases you can overload the processors on devices. When this happens you may need to lower cpu burden by lowering encryption standards

Or you may need to integrate an older device to your network. 
In any case you can change the complexity levels from the yaml file. 
After you do a change in yaml make sure that you note the date because after the change every new tunnel is going to have a different configuration

The guts of file are pretty self explanatory. 


### todo 
- Certificate generation and auto upload.
- Selector based vpn tunnels
- Auto rule creation
- Auto Route creation