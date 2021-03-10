from google.protobuf.text_format import MessageToString

from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.identity.account.notify_account_pb2_grpc import NotifyAccountServiceServicer
from support.notifications.apple_push_notifications import ApplePushNotifications


class NotifyAccountService(NotifyAccountServiceServicer):
    def __init__(self):
        super(NotifyAccountService, self).__init__()
        self.session_scope = self.__class__.__name__

    def NewReceivedMessageFromAccountAssistant(self, request, context):
        print("NotifyAccountService:NewReceivedMessageFromAccountAssistant")
        ios_new_messages_payload = {
            'aps': {
                'alert': "Received new messages",
                'sound': "default",
                'badge': 1,
            },
            'account_id': request.account_id,
            'connected_account_assistant': MessageToString(request.connected_account_assistant, as_one_line=True),
            'account_assistant_received_message_id': request.account_assistant_received_message_id
        }
        try:
            apns = ApplePushNotifications()
            apns.notify_account(account_id=request.account_id, payload=ios_new_messages_payload)
            print("DEBUG:: NOTIFICATION SENT")
            return ResponseMeta(meta_done=True, meta_message="Notified successfully!")
        except:
            print("DEBUG:: NOTIFICATION NOT SENT")
            return ResponseMeta(meta_done=False, meta_message="Couldn't notify account!")
