#   /*************************************************************************
#   *
#   * AMIT KUMAR KHETAN CONFIDENTIAL
#   * __________________
#   *
#   *  [2017] - [2021] Amit Kumar Khetan
#   *  All Rights Reserved.
#   *
#   * NOTICE:  All information contained herein is, and remains
#   * the property of Amit Kumar Khetan and its suppliers,
#   * if any.  The intellectual and technical concepts contained
#   * herein are proprietary to Amit Kumar Khetan
#   * and its suppliers and may be covered by U.S. and Foreign Patents,
#   * patents in process, and are protected by trade secret or copyright law.
#   * Dissemination of this information or reproduction of this material
#   * is strictly forbidden unless prior written permission is obtained
#   * from Amit Kumar Khetan.
#   */

import json
import socket
import ssl
import struct

# --------------- input ---------------
test = False
account_device_token = "b4b58402d2368fdce4112ea2f3d97c1e53347a82f6658d29b0550066c34f306e"
rpc_index = 3
silent = True
title = ""
body = ""
badge = 0
# --------------- input ---------------

if rpc_index == 1:
    rpc = "SyncAccountSentMessagesNotification"
elif rpc_index == 2:
    rpc = "SyncAccountReceivedMessagesNotification"
elif rpc_index == 3:
    rpc = "SyncAccountConnectionsNotification"

if test:
    host = "gateway.sandbox.push.apple.com"
    port = int("2195")
    certificate = "/opt/ethos/wiki/eapp-wiki/config/keys/apns_cert.pem"
else:
    host = "gateway.push.apple.com"
    port = int("2195")
    certificate = "/Users/amitkumarkhetan/Desktop/iEthosProdAPNSCert.pem"

apns_address = (host, port)
socket = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), certfile=certificate)
socket.connect(apns_address)
byte_account_device_token = bytes.fromhex(account_device_token.replace(' ', ''))

if silent:
    aps = {
        "content-available": 1,
        'badge': badge,
    }
else:
    aps = {
        'alert': {
            "title": title,
            "body": body,
        },
        'sound': "default",
        'badge': badge,
    }

    payload = {
        'aps': {
            "alert": {
                "title": "You're now connected to Rushali",
                "body": "Start your conversation here",
            },
            'sound': "default",
            'badge': 0,
        },
        'service': "NotifyAccountService",
        'rpc': rpc
    }

ios_payload = {
    'aps': aps,
    'service': "NotifyAccountService",
    'rpc': rpc,
}
encoded_payload = json.dumps(ios_payload).encode('utf-8')

notification_format = '!BH32sH%ds' % len(encoded_payload)
notification = struct.pack(notification_format, 0, 32, byte_account_device_token, len(encoded_payload),
                           encoded_payload)
print(f"writing to socket: {socket.write(notification)}")
socket.close()
