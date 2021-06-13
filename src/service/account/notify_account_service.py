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

import logging
import os

from google.protobuf.text_format import MessageToString
from pyfcm import FCMNotification

from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.identity.account.notify_account_pb2_grpc import NotifyAccountServiceServicer
from services_caller.account_service_caller import get_account_by_id_caller
from support.db_service import get_account_device_token
from support.notifications.apple_push_notifications import ApplePushNotifications


class NotifyAccountService(NotifyAccountServiceServicer):
    def __init__(self):
        super(NotifyAccountService, self).__init__()
        self.session_scope = self.__class__.__name__

    def NewReceivedMessageFromAccountAssistant(self, request, context):
        logging.info("NotifyAccountService:NewReceivedMessageFromAccountAssistant")
        ios_new_messages_payload = {
            'aps': {
                'alert': "You've received new messages from account assistants",
                'sound': "default",
                'badge': 0,
            },
            'account_id': request.account_id,
            'connected_account_assistant': MessageToString(request.connected_account_assistant, as_one_line=True),
            'account_assistant_received_message_id': request.account_assistant_received_message_id
        }
        try:
            apns = ApplePushNotifications()
            apns.notify_account(account_id=request.account_id, payload=ios_new_messages_payload)
            logging.info("DEBUG:: NOTIFICATION SENT")
            return ResponseMeta(meta_done=True, meta_message="Notified successfully!")
        except:
            logging.info("DEBUG:: NOTIFICATION NOT SENT")
            return ResponseMeta(meta_done=False, meta_message="Couldn't notify account!")

    def NewReceivedMessageFromAccount(self, request, context):
        logging.info("NotifyAccountService:NewReceivedMessageFromAccount")
        account, _, _ = get_account_by_id_caller(account_id=request.connecting_account_id)
        # ios_new_messages_payload = {
        #     'aps': {
        #         'alert': {
        #             "title": f"{account.account_first_name} {account.account_last_name}",
        #             "body": f"{request.message}",
        #         },
        #         'sound': "default",
        #         'badge': 0,
        #     },
        #     'account_id': request.account_id,
        #     'service': "NotifyAccountService",
        #     'rpc': "NewReceivedMessageFromAccount"
        # }
        try:
            # apns = ApplePushNotifications()
            message_title = f"{account.account_last_name.strip()[0]}, {account.account_first_name}"
            message_body = request.message
            message_data = {
                'account_id': request.account_id,
                'service': "NotifyAccountService",
                'rpc': "NewReceivedMessageFromAccount"
            }
            push_service = FCMNotification(api_key=os.environ['FCM_API_KEY'])
            push_result = push_service.notify_single_device(
                registration_id=get_account_device_token(account_id=request.account_id),
                message_title=message_title,
                message_body=message_body,
                data_message=message_data, sound='Default'
            )
            # apns.notify_account(account_id=request.account_id, payload=ios_new_messages_payload)
            logging.info("DEBUG:: NOTIFICATION SENT")
            return ResponseMeta(meta_done=True, meta_message="Notified successfully!")
        except Exception as e:
            logging.info(f" notification is not sent, Exception: {e}")
            return ResponseMeta(meta_done=False, meta_message="Couldn't notify account!")

    def AccountConnectedAccountNotification(self, request, context):
        logging.info("NotifyAccountService:AccountFullyConnectedWithAccount")
        connecting_account, _, _ = get_account_by_id_caller(
            account_id=request.connecting_account_connected_account.account_id)

        title = ""
        body = ""
        if request.connecting_account_connected_account.account_interested_in_connection:
            if request.connecting_account_connected_account.connected_account_interested_in_connection:
                title = f"You're now connected to {connecting_account.account_first_name}"
                body = f"Start your conversation here"
        else:
            if request.connecting_account_connected_account.connected_account_interested_in_connection:
                title = f"{request.account.account_first_name} is interested in connecting with you"
                body = f"Connect to start your conversation here"

        if title != "" and body != "":
            aps = {
                'alert': {
                    "title": title,
                    "body": body,
                },
                'sound': "default",
                'badge': 0,
            }
        else:
            aps = {
                "content-available": 1,
                'sound': "default",
                'badge': 0,
            }
        try:
            ios_payload = {
                'aps': aps,
                'account_id': request.account.account_id,
                'service': "NotifyAccountService",
                'rpc': "AccountConnectedAccountNotification",
                "connecting_account_connected_account": request.connecting_account_connected_account.SerializeToString()
            }
            apns = ApplePushNotifications()
            apns.notify_account(account_id=request.account.account_id, payload=ios_payload)
            logging.info("NotifyAccountService:NewReceivedMessageFromAccountAssistant: "
                         "notification sent")
            return ResponseMeta(meta_done=True, meta_message="Notified successfully!")
        except Exception as e:
            logging.info(f"NotifyAccountService:NewReceivedMessageFromAccountAssistant: "
                         f"notification is not sent, Exception: {e}")
            return ResponseMeta(meta_done=False, meta_message="Couldn't notify account!")
