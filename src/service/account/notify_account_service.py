import logging

from google.protobuf.text_format import MessageToString

from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.identity.account.notify_account_pb2_grpc import NotifyAccountServiceServicer
from services_caller.account_service_caller import get_account_by_id_caller
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
        ios_new_messages_payload = {
            'aps': {
                'alert': {
                    "title": f"{account.account_first_name} {account.account_last_name}",
                    "body": f"{request.message}",
                },
                'sound': "default",
                'badge': 0,
            },
            'account_id': request.account_id,
            'service': "NotifyAccountService",
            'rpc': "ListenForReceivedAccountMessages"
        }
        try:
            apns = ApplePushNotifications()
            apns.notify_account(account_id=request.account_id, payload=ios_new_messages_payload)
            logging.info("DEBUG:: NOTIFICATION SENT")
            return ResponseMeta(meta_done=True, meta_message="Notified successfully!")
        except:
            logging.info("DEBUG:: NOTIFICATION NOT SENT")
            return ResponseMeta(meta_done=False, meta_message="Couldn't notify account!")
