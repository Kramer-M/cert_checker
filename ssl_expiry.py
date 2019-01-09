# Author: Lucas Roelser <roesler.lucas@gmail.com>
# Modified from serverlesscode.com/post/ssl-expiration-alerts-with-lambda/

import datetime
import fileinput
import logging
import os
import socket
import ssl
import time

logger = logging.getLogger('SSLVerify')

def ssl_expiry_datetime(hostname: str, port: int) -> datetime.datetime:
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )
    # 3 second timeout because Lambda has runtime limitations
    # conn.settimeout(3.0)

    logger.debug('Connect to {}'.format(hostname))
    conn.connect((hostname, port))
    ssl_info = conn.getpeercert()
    # parse the string from the certificate into a Python datetime object
    return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)


def ssl_valid_time_remaining(hostname: str, port: int) -> datetime.timedelta:
    # Get the number of days left in a cert's lifetime.
    expires = ssl_expiry_datetime(hostname, port)
    logger.debug(
        'SSL cert for {} expires at {}'.format(
            hostname, expires.isoformat()
        )
    )
    return expires - datetime.datetime.utcnow()


# def test_host(hostname: str, buffer_days: int=30) -> str:
#     # return test message for hostname cert expiration.
#     try:
#         will_expire_in = ssl_valid_time_remaining(hostname, port)
#     except ssl.certificateerror as e:
#         return f'{hostname} cert error {e}'
#     except ssl.sslerror as e:
#         return f'{hostname} cert error {e}'
#     except socket.timeout as e:
#         return f'{hostname} could not connect'
#     else:
#         if will_expire_in < datetime.timedelta(days=0):
#             return f'{hostname} cert will expired'
#         elif will_expire_in < datetime.timedelta(days=buffer_days):
#             return f'{hostname} cert will expire in {will_expire_in}'
#         else:
#             return f'{hostname} cert is fine'

# print(ssl_valid_time_remaining("cms8800.wdf.sap.corp"))
