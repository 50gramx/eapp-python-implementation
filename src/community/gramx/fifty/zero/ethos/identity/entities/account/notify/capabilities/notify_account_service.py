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

import firebase_admin
from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.identity.account.notify_account_pb2_grpc import NotifyAccountServiceServicer
from firebase_admin import messaging
from pyfcm import FCMNotification

from community.gramx.fifty.zero.ethos.identity.services_caller.account_assistant_service_caller import \
    get_account_assistant_name_code_by_id
from community.gramx.fifty.zero.ethos.identity.services_caller.account_service_caller import get_account_by_id_caller, \
    validate_account_services_caller
from support.application.tracing import trace_rpc
from support.database.account_devices_services import get_account_device_token, update_account_devices
from support.helper_functions import format_timestamp_to_datetime


# TODO: ADD APP SOUNDS

class NotifyAccountService(NotifyAccountServiceServicer):
    def __init__(self):
        super(NotifyAccountService, self).__init__()
        self.session_scope = self.__class__.__name__
        self.fcm_push_service = FCMNotification(api_key=os.environ['FCM_API_KEY'])
        self.app = firebase_admin.initialize_app()

    @trace_rpc()
    def NewReceivedMessageFromAccountAssistant(self, request, context):
        logging.info("NotifyAccountService:NewReceivedMessageFromAccountAssistant")
        assistant_name_code, assistant_name = get_account_assistant_name_code_by_id(
            account_assistant_id=request.connecting_account_assistant_id)
        # ios_new_messages_payload = {
        #     'aps': {
        #         'alert': "You've received new messages from account assistants",
        #         'sound': "default",
        #         'badge': 0,
        #     },
        #     'account_id': request.account_id,
        #     'connected_account_assistant': MessageToString(request.connected_account_assistant, as_one_line=True),
        #     'account_assistant_received_message_id': request.account_assistant_received_message_id
        # }
        message_title = f"#{assistant_name_code} {assistant_name}"
        message_body = f"{request.message}"
        message_data = {
            'account_id': request.account_id,
            'service': "NotifyAccountService",
            'rpc': "NewReceivedMessageFromAccountAssistant",
        }
        try:
            # See documentation on defining a message payload.
            message = messaging.Message(
                notification=messaging.Notification(
                    title=message_title,
                    body=message_body,
                ),
                data=message_data,
                token=get_account_device_token(account_id=request.account_id),
            )
            push_result = messaging.send(message)
            logging.info(f"DEBUG:: NOTIFICATION SENT: {push_result}")
            return ResponseMeta(meta_done=True, meta_message="Notified successfully!")
        except:
            logging.info("DEBUG:: NOTIFICATION NOT SENT")
            return ResponseMeta(meta_done=False, meta_message="Couldn't notify account!")

    @trace_rpc()
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
            message_title = f"{account.account_first_name} {account.account_last_name.strip()}"
            message_body = request.message
            message_data = {
                'account_id': request.connecting_account_id,
                'service': "NotifyAccountService",
                'rpc': "NewReceivedMessageFromAccount"
            }
            message = messaging.Message(
                notification=messaging.Notification(
                    title=message_title,
                    body=message_body,
                ),
                data=message_data,
                token=get_account_device_token(account_id=request.account_id),
            )
            push_result = messaging.send(message)
            # apns.notify_account(account_id=request.account_id, payload=ios_new_messages_payload)
            logging.info(f"DEBUG:: NOTIFICATION SENT: {push_result}")
            return ResponseMeta(meta_done=True, meta_message="Notified successfully!")
        except Exception as e:
            logging.info(f" notification is not sent, Exception: {e}")
            return ResponseMeta(meta_done=False, meta_message="Couldn't notify account!")

    @trace_rpc()
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
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                data=ios_payload,
                token=get_account_device_token(account_id=request.account_id),
            )
            push_result = messaging.send(message)
            logging.info(f"NotifyAccountService:NewReceivedMessageFromAccountAssistant: "
                         f"notification sent {push_result}")
            return ResponseMeta(meta_done=True, meta_message="Notified successfully!")
        except Exception as e:
            logging.info(f"NotifyAccountService:NewReceivedMessageFromAccountAssistant: "
                         f"notification is not sent, Exception: {e}")
            return ResponseMeta(meta_done=False, meta_message="Couldn't notify account!")

    @trace_rpc()
    def UpdateAccountDeviceDetails(self, request, context):
        logging.info("NotifyAccountService:AccountFullyConnectedWithAccount")
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return response_meta
        else:
            update_account_devices(
                account_id=request.access_auth_details.account.account_id,
                account_device_os=request.account_device_details.account_device_os,
                account_device_token=request.account_device_details.device_token,
                account_device_token_accessed_at=format_timestamp_to_datetime(request.access_auth_details.requested_at)
            )
            return response_meta
