#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script creates vpn tunnels for fortios firewall devices
"""

__author__      = "Mesut Bayrak"
__copyright__ = "Copyright 2016, Planet Earth"


import argparse, secrets, string, paramiko, time, logging

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


parser = argparse.ArgumentParser(description='Creates vpn tunnels')


parser.add_argument('-C','--create',
                    nargs='+',
                    required=False,
                    help='vpn tunnel creator requires 6 parameters name, interfece,remote gatewayip, source net, destination net')

parser.add_argument('-D','--delete',
                    required=False,
                    help='tunnel delete requires 1 paramaeter which is the name of tunnel')

parser.add_argument('-L','--list',
                    required=False,
                    help='lists vpn tunnels requires no parameter --detail shows tunnel status')

parser.add_argument('-S','--selector',
                    required=False,
                    help='Switch for selector based tunnels')

args = parser.parse_args()

if args.create:
    print("your password is :", generatedpsk(16))

    Script1 = ['config vpn ipsec phase1-interface\n',
               'edit Datacenter\n',
               'set forticlient-enforcement asd\n']
    Script2 = ['get system status\n',]

    Script3 = ['config vpn ipsec phase1-interface',
               'edit "Datacenter',
               'set interface "wan1"',
               'set ike-version 2',
               'set dhgrp 2',
               'set proposal 3des-md5',
               'set remote-gw 185.141.110.220',
               'set psksecret ENC 24l+Ll/2UUxhMVZKebtODmW3etuRWxiZ0xR4ZMNyXFmPPRv9jDblOnDP3Inb6HnAA7jbzeQQaxosCLEp7BVYnhZn/TF/Eu+p2rLHDn0oK+h0dBBK'
               'next',
               'end',
               'config vpn ipsec phase2-interface',
               'edit "datacenter"',
               'set keepalive enable',
               'set phase1name "Datacenter"',
               'set proposal 3des-sha1',
               'set dhgrp 14',
               'next',
               'end']

    test = SendAndCheck('192.168.17.1', '2222', 'testuser', '12qwasZX', Script1)
    print(test)

elif args.delete:
    print("delete")

elif args.list:
    print('list')


