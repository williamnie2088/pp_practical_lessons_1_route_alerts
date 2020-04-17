#!/usr/bin/env python

from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
import os
from twilio.rest import Client

# SMS related configuraiton
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
from_number = os.environ['TWILIO_FROM_NUM']
to_number = os.environ['TWILIO_TO_NUM']

client = Client(account_sid, auth_token)

# Route detection related configuraiton
nr = InitNornir()

# Step 1. create a function for commands
def run_command(command):
    result = nr.run(task=netmiko_send_command, command_string=command)
    return result


watched_routes = ['192.168.0.13']

my_result = run_command('show ip route')
for device in my_result:
    print(device + ":")
    for output in my_result[device]:
        for route in watched_routes:
            if route in str(output):
                print('Nice, the route is there.')
            else:
                print('Oh no, time to troubleshoot!')
                message = client.messages \
                    .create(
                    body="Kevin Bacon needs you to troubleshoot " + str(device),
                    from_=from_number,
                    to=to_number
                )



