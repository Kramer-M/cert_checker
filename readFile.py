# Author: Lucas Roelser <roesler.lucas@gmail.com>
# Modified from serverlesscode.com/post/ssl-expiration-alerts-with-lambda/

import datetime
import fileinput
import logging
import os
import socket
import ssl
import time
from ssl_expiry import *
from sendMail import *

# Read in the Certificate target file
filename = "input.txt"
if not os.path.isfile(filename):
    exit()

with open(filename, encoding='utf-8-sig') as f:
    lines = (line.strip() for line in f)
    # ignore blank lines with this generator expression
    lines = (line for line in lines if line) 
    # ignore comments (inline comments might be a problem!)
    lines = (line for line in lines if not line.startswith("#")) 
    # remove the https from the urls, maybe add one for http
    lines = (line.replace("https://","") for line in lines)
    # create list element out of the generator 
    lines = list(lines)

# call ssl checker and get remaining days
for line in lines:
    arg = line.split(';')

    # get the port number if necessary
    try:
        hostname,port = arg[0].split(':')
        port = int(port)
    except ValueError:
        logger.debug("No explicit port found")
        hostname = arg[0]
        port = 443

    days = int(arg[1])

    # now get remaining days
    try:
        rem_days = ssl_valid_time_remaining(hostname, port).days
        #?print(rem_days, days)
    except Exception as e:
        textbody = "Error for url '{}': \n \t {}".format(arg[0], e)
        print(textbody)
        #!check_and_send_mail('serdar.asan@sap.com', textbody)
        #?check_and_send_mail('manuel.kramer01@sap.com', textbody)
        
    # compare days and send email if they disagree
    # according to mail smaller than 60
    if rem_days < 60: 
        textbody = "Warning for url '{}': \n \t valid remainig days [{}] are smaller than 60.".format(hostname, rem_days)
        print(textbody)
        #!check_and_send_mail('serdar.asan@sap.com', textbody)
        #?check_and_send_mail('manuel.kramer01@sap.com', textbody)
    


