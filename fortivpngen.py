#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script creates vpn tunnels for fortios firewall devices
"""

__author__      = "Mesut Bayrak"
__copyright__ = "Copyright 2016, Planet Earth"


import argparse, secrets, string, paramiko, time, logging, yaml

def config_data():
    with open('./config.yml', 'r') as ymlfile:
        config_data = yaml.load(ymlfile)
    return config_data


def SendAndCheck(_host,_port,_username,_password,_command):
    logging.getLogger("paramiko").setLevel(logging.DEBUG)  # for example
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(_host, _port, _username, _password, allow_agent=False,look_for_keys=False)
    print('connection to Fortigate established')
    # print('item count :',len(_command),_command)
    channel = ssh.invoke_shell()
    item_number=0
    output_list=''
    for item in _command:

        print('log output', output_list)
        print('positive action chosen cycle :', item_number)
        print('the command to send :', _command[item_number])

        # Sending command
        corrected_command = str(_command[item_number])
        channel.send(corrected_command)
        time.sleep(1)

        # command sent receiving output
        output = channel.recv(2048)
        new_text = str(output)
        remove_trails = new_text.split('\\r')
        output_list = [item.strip('\\n') for item in remove_trails]

        # Error checking
        if 'Command fail.' in str(output_list):
            print('Command fail catched', str(output_list))
            print('error in command closing channel')
            success = False
            return success
        if  'Unknown action' in str(output_list):
            print('Unknown action catched', str(output_list))
            print('error in command closing channel')
            success = False
            # return success
        else:
            print(str(output_list))
            print('command sent\n\n')
            item_number = item_number + 1
            success = True
    channel.close()
    ssh.close()
    return success

def ListTunnels(_host,_port,_username,_password,_command):
    logging.getLogger("paramiko").setLevel(logging.DEBUG)  # for example
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(_host, _port, _username, _password, allow_agent=False,look_for_keys=False)
    print('connection to Fortigate established')
    # print('item count :',len(_command),_command)
    channel = ssh.invoke_shell()
    item_number=0
    output_list=''
    for item in _command:

        print('log output', output_list)
        print('positive action chosen cycle :', item_number)
        print('the command to send :', _command[item_number])

        # Sending command
        corrected_command = str(_command[item_number])
        channel.send(corrected_command)
        time.sleep(1)

        # command sent receiving output
        output = channel.recv(2048)
        new_text = str(output)
        remove_trails = new_text.split('\\r')
        output_list = [item.strip('\\n') for item in remove_trails]

        # Error checking
        if 'Command fail.' in str(output_list):
            print('Command fail catched', str(output_list))
            print('error in command closing channel')
            success = False
            return success
        if  'Unknown action' in str(output_list):
            print('Unknown action catched', str(output_list))
            print('error in command closing channel')
            success = False
            # return success
        else:
            print(str(output_list))
            print('command sent\n\n')
            item_number = item_number + 1
            success = True
    channel.close()
    ssh.close()
    return output_list

def generatedpsk(secret_length):
    stringSource = string.ascii_letters + string.digits + string.punctuation
    password = secrets.choice(string.ascii_lowercase)
    password += secrets.choice(string.ascii_uppercase)
    password += secrets.choice(string.digits)
    password += secrets.choice(string.punctuation)
    for i in range(secret_length):
        password += secrets.choice(stringSource)
    char_list = list(password)
    secrets.SystemRandom().shuffle(char_list)
    password = ''.join(char_list)
    return password

#Read config data from yml
config = config_data()

#Structure parameter processing

parser = argparse.ArgumentParser(description='Creates vpn tunnels')


parser.add_argument('-C','--create',
                    nargs='+',
                    required=False,
                    help='vpn tunnel creator requires 5 parameters name, interfece,remote gatewayip, source net, destination net')

parser.add_argument('-D','--delete',
                    required=False,
                    help='tunnel delete requires 1 paramaeter which is the name of tunnel')

parser.add_argument('-L','--list',
                    required=False,
                    action='store_true',
                    help='lists vpn tunnels requires no parameter --detail shows tunnel status')

parser.add_argument('-V','--verbose',
                    required=False,
                    help='Start verbose logging to stdout')

args = parser.parse_args()


#Switch operations

if args.create:
    _tunnelname = args.create[0]
    _tunnelint= args.create[1]
    _tunneldest= args.create[2]
    _tunnellocal = args.create[3]
    _tunnelremote = args.create[4]

    #Construtction of script for vpn
    _Script_add_tunnel = ['config vpn ipsec phase1-interface'+'\n',
               'edit '+_tunnelname+'\n',
               'set interface '+_tunnelint+'\n',
               'set '+ config['Phase1-interface']['ikever']+'\n',
               'set '+ config['Phase1-interface']['dhgrp']+'\n',
               'set proposal '+config['Phase1-interface']['proposal']+'\n',
               'set remote-gw '+ _tunneldest+'\n',
               'set psk '+generatedpsk(16)+'\n',
               'end'+'\n',
               'config vpn ipsec phase2-interface'+'\n',
               'edit '+_tunnelname+'-p2\n',
               'set keepalive '+config['Phase2-interface']['keepalive']+'\n',
               'set phase1name '+_tunnelname+'\n',
               'set proposal '+config['Phase2-interface']['proposal']+'\n',
               'set '+config['Phase2-interface']['dhgrp']+'\n',
               'next'+'\n',
               'end'+'\n',]

    _Script_add_tunnel_with_route = ['config vpn ipsec phase1-interface' + '\n',
                                     'edit ' + _tunnelname + '\n',
                                     'set interface ' + _tunnelint + '\n',
                                     'set ' + config['Phase1-interface']['ikever'] + '\n',
                                     'set ' + config['Phase1-interface']['dhgrp'] + '\n',
                                     'set proposal ' + config['Phase1-interface']['proposal'] + '\n',
                                     'set remote-gw ' + _tunneldest + '\n',
                                     'set psk ' + generatedpsk(16) + '\n',
                                     'end' + '\n',
                                     'config vpn ipsec phase2-interface' + '\n',
                                     'edit ' + _tunnelname + '-p2\n',
                                     'set keepalive ' + config['Phase2-interface']['keepalive'] + '\n',
                                     'set phase1name ' + _tunnelname + '\n',
                                     'set proposal ' + config['Phase2-interface']['proposal'] + '\n',
                                     'set ' + config['Phase2-interface']['dhgrp'] + '\n',
                                     'next' + '\n',
                                     'end' + '\n',
                                     'config router static',
                                     'edit ' + config['Staticroute']['prefix'] + '\n',
                                     'set comment "' + _tunnelname + _tunnelremote + '\n',
                                     'set device ' + _tunnelname + '\n',
                                     'set dst ' + _tunnelremote + '\n',
                                     'next']

    #Read credential config
    _firewall = config['Credentials']['firewall']
    _fwport = config['Credentials']['port']
    _fwuser = config['Credentials']['user']
    _fwpass = config['Credentials']['pass']

    addnew_tunnel = SendAndCheck(_firewall, _fwport, _fwuser, _fwpass, _Script_add_tunnel)
    print(_firewall, _fwport, _fwuser, _fwpass, _Script_add_tunnel)
    print(addnew_tunnel)

elif args.delete:
    print("delete")

elif args.list:
    print('list')
    _Script_Get_Tunnels = ['get vpn ipsec tunnel summary' + '\n',]

    # Read credential config
    _firewall = config['Credentials']['firewall']
    _fwport = config['Credentials']['port']
    _fwuser = config['Credentials']['user']
    _fwpass = config['Credentials']['pass']

    get_tunnels = ListTunnels(_firewall, _fwport, _fwuser, _fwpass, _Script_Get_Tunnels)
    print(_firewall, _fwport, _fwuser, _fwpass, _Script_Get_Tunnels)
    print(get_tunnels)


