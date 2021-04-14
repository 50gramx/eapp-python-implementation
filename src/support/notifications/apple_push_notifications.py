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
import os
import socket
import ssl
import struct

from support.db_service import get_account_device_token


class ApplePushNotifications(object):

    def __init__(self):
        self.host = os.environ['APPLE_PUSH_NOTIFICATION_HOST']
        self.port = int(os.environ['APPLE_PUSH_NOTIFICATION_PORT'])
        self.certificate = os.environ['APPLE_PUSH_NOTIFICATION_CERTIFICATE']
        self.apns_address = (self.host, self.port)
        self.socket = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), certfile=self.certificate)
        self.socket.connect(self.apns_address)

    def notify_account(self, account_id: str, payload):
        account_device_token = get_account_device_token(account_id=account_id)
        print(f"DEBUG:: DEVICE TOKEN: {account_device_token}")
        byte_account_device_token = bytes.fromhex(account_device_token.replace(' ', ''))

        encoded_payload = json.dumps(payload).encode('utf-8')

        notification_format = '!BH32sH%ds' % len(encoded_payload)
        notification = struct.pack(notification_format, 0, 32, byte_account_device_token, len(encoded_payload),
                                   encoded_payload)

        self.socket.write(notification)
        self.socket.close()
