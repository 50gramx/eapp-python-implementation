import logging

import phonenumbers

from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.identity.account.connect_account_pb2 import ConnectedAccountAssistants, \
    ConnectedAccounts, SyncAccountConnectionsResponse, ConnectAccountResponse
from ethos.elint.services.product.identity.account.connect_account_pb2_grpc import ConnectAccountServiceServicer
from models.account_connection_models import AccountConnections
from services_caller.account_service_caller import validate_account_services_caller, \
    is_account_exists_with_mobile_caller, connect_account_caller
from support.db_service import get_account
from support.helper_functions import gen_uuid


class ConnectAccountService(ConnectAccountServiceServicer):
    def __init__(self):
        super(ConnectAccountService, self).__init__()
        self.session_scope = self.__class__.__name__

    def GetAllConnectedAccountAssistants(self, request, context):
        logging.info("ConnectAccountService:GetAllConnectedAccountAssistants")
        access_done, access_message = validate_account_services_caller(request)
        meta = ResponseMeta(meta_done=access_done, meta_message=access_message)
        if access_done is False:
            return ConnectedAccountAssistants(response_meta=meta)
        else:
            account_connections = AccountConnections(account_id=request.account.account_id)
            list_of_connected_account_assistants = account_connections.get_connected_account_assistants()
            return ConnectedAccountAssistants(
                connected_account_assistants=list_of_connected_account_assistants, response_meta=meta)

    def IsAccountAssistantConnected(self, request, context):
        logging.info("ConnectAccountService:IsAccountAssistantConnected")
        account_connections = AccountConnections(account_id=request.account_id)
        account_assistant_connected = account_connections.is_account_assistant_connected(
            account_assistant_connection_id=request.connected_account_assistant.account_assistant_connection_id,
            account_assistant_id=request.connected_account_assistant.account_assistant_id
        )
        if account_assistant_connected is False:
            return ResponseMeta(meta_done=account_assistant_connected, meta_message="Account Assistant not connected.")
        else:
            return ResponseMeta(meta_done=account_assistant_connected, meta_message="Account Assistant connected.")

    def GetAllConnectedAccounts(self, request, context):
        logging.info("ConnectAccountService:GetAllConnectedAccounts")
        access_done, access_message = validate_account_services_caller(request)
        if access_done is False:
            return ConnectedAccounts(
                response_meta=ResponseMeta(meta_done=access_done, meta_message=access_message))
        else:
            account_connections = AccountConnections(account_id=request.account.account_id)
            list_of_connected_accounts = account_connections.get_connected_accounts()
            return ConnectedAccounts(
                connected_accounts=list_of_connected_accounts,
                response_meta=ResponseMeta(meta_done=access_done, meta_message=access_message))

    def IsAccountConnected(self, request, context):
        logging.info("ConnectAccountService:IsAccountConnected")
        account_connections = AccountConnections(account_id=request.account_id)
        is_account_connected = account_connections.is_account_connected(
            account_connection_id=request.connected_account.account_connection_id,
            account_id=request.connected_account.account_id
        )
        if is_account_connected:
            return ResponseMeta(meta_done=True, meta_message="Account connected.")
        else:
            return ResponseMeta(meta_done=False, meta_message="Account not connected.")

    def ConnectAccount(self, request, context):
        logging.info("ConnectAccountService:ConnectAccount")
        access_done, access_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=access_done, meta_message=access_message)
        if access_done is False:
            return ConnectAccountResponse(response_meta=response_meta)
        else:
            account_connections = AccountConnections(account_id=request.access_auth_details.account.account_id)
            connecting_account_connections = AccountConnections(account_id=request.connecting_account_id)
            is_account_connection_exists = account_connections.is_account_connection_exists(
                account_id=request.connecting_account_id)
            if is_account_connection_exists:
                connected_account = account_connections.get_connected_account(account_id=request.connecting_account_id)
                if not connected_account.account_interested_in_connection:
                    account_connections.update_account_interest_in_connection(account_id=request.connecting_account_id,
                                                                              is_interested=True)
                    connecting_account_connections.update_connected_account_interest_in_connection(
                        account_id=request.access_auth_details.account.account_id, is_interested=True)
                connected_account = account_connections.get_connected_account(
                    account_id=request.connecting_account_id)
                return ConnectAccountResponse(
                    connected_account=connected_account,
                    response_meta=ResponseMeta(meta_done=True, meta_message="Account connection exists.")
                )
            else:
                new_connection_id = gen_uuid()
                account_connections.add_new_account_connection(
                    account_connection_id=new_connection_id,
                    account_id=request.connecting_account_id,
                    self_connecting=True
                )
                connecting_account_connections.add_new_account_connection(
                    account_connection_id=new_connection_id,
                    account_id=request.access_auth_details.account.account_id,
                    self_connecting=False
                )
                connected_account = account_connections.get_connected_account(account_id=request.connecting_account_id)
                return ConnectAccountResponse(
                    connected_account=connected_account,
                    response_meta=ResponseMeta(meta_done=True, meta_message="Account connected")
                )

    def SyncAccountConnections(self, request, context):
        logging.info("ConnectAccountService:SyncAccountConnections")
        access_done, access_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=access_done, meta_message=access_message)
        if access_done is False:
            return SyncAccountConnectionsResponse(response_meta=response_meta)
        else:
            # list_of_exception_accounts = ["+91 832 755 8649", "97767 76943", "70089 40679", "83389 44408",
            #                               "96925 45414", "+91 87630 79777", "97 76 776943", "+917008940679",
            #                               "977-677-6943", "+919439098001", "97767 76943"]
            connected_account_mobile_numbers = []
            connected_accounts = []
            for connecting_account_mobile_number in request.connecting_account_mobile_numbers:
                if len(connecting_account_mobile_number) >= 10:
                    try:
                        account_country_code = "+" + str(
                            phonenumbers.parse(connecting_account_mobile_number, "IN").country_code)
                        account_mobile_number = str(
                            phonenumbers.parse(connecting_account_mobile_number, "IN").national_number)
                        if request.access_auth_details.account.account_mobile_number != account_mobile_number and account_mobile_number not in connected_account_mobile_numbers:
                            is_account_exists_with_mobile, meta_message = is_account_exists_with_mobile_caller(
                                access_auth_details=request.access_auth_details,
                                account_country_code=account_country_code,
                                account_mobile_number=account_mobile_number
                            )
                            if is_account_exists_with_mobile:
                                try:
                                    connecting_account = get_account(account_mobile_number=account_mobile_number)
                                    is_account_connected, account_connected_message, connected_account = connect_account_caller(
                                        access_auth_details=request.access_auth_details,
                                        connecting_account_id=connecting_account.account_id)
                                    if is_account_connected is True:
                                        connected_account_mobile_numbers.append(account_mobile_number)
                                        connected_accounts.append(SyncAccountConnectionsResponse.ConnectedAccount(
                                            connected_account=connected_account,
                                            connecting_account_mobile_number=connecting_account_mobile_number))
                                    else:
                                        pass
                                except AttributeError:
                                    logging.error(f"Attribute Error: {account_mobile_number}")

                            else:
                                pass
                    except phonenumbers.phonenumberutil.NumberParseException:
                        logging.exception("Not a valid number")
            return SyncAccountConnectionsResponse(connected_accounts=connected_accounts, response_meta=response_meta)
