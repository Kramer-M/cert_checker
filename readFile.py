import datetime
import fileinput
import logging
import os
import socket
import ssl
import time
from ssl_expiry import *
from sendOutlookMail import *

# initialize log file
#logging.basicConfig(filename='CertificateChecker.log', format='%(asctime)s %(message)s: %(levelname)s', filemode='w', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', filemode='w', level=logging.DEBUG)
logging.info("Start Program")

# Read in the Certificate target file
filename = "input.txt"
if not os.path.isfile(filename):
    logging.error("{} not found. Please make sure it is in the same directory".format(filename))
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
    logging.info("Start to check Certificate for {}".format(arg[0]))

    # get the port number if necessary
    try:
        hostname,port = arg[0].split(':')
        port = int(port)
    except ValueError:
        logger.debug("No explicit port found")
        hostname = arg[0]
        port = 443

    mailRecipient = arg[2]
    daysFile = int(arg[1])
    
    # reset flag
    flag = False 
    # now get remaining days
    try:
        date = ssl_expiry_datetime(hostname, port)
        rem_days = int((date - datetime.datetime.utcnow()).days)
        flag = True

    except Exception as e:
        textbody = "Error for url '{}': \n \t {}".format(hostname, e)
        logging.error(textbody)
        check_and_send_mail(mailRecipient, textbody)
        #?check_and_send_mail('manuel.kramer01@sap.com', textbody)
        
    # compare days and send email if they disagree
    # according to mail smaller than 60, check if 
    if flag:
        if rem_days < daysFile: 
            textbody = "Warning for url '{}': \n \t Certificate will expire in {} days. \n \t Date of expiration: {}\n \t Warning for expiration check is set to {} days.".format(hostname, rem_days, date, daysFile)
            logging.warning(textbody)
            check_and_send_mail(mailRecipient, textbody)
        else:
            logging.debug("No mail sent because certificate won't expire within {} days. Certificate will be valid until {}".format(daysFile, date))
    
logging.info("End Program")


