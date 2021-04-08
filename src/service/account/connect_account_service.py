import logging

import phonenumbers

from ethos.elint.entities.account_pb2 import AccountMobile
from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.identity.account.connect_account_pb2 import ConnectedAccountAssistants, \
    ConnectedAccounts, ConnectAccountResponse, ParseAccountMobilesResponse, SyncAccountConnectionsResponse
from ethos.elint.services.product.identity.account.connect_account_pb2_grpc import ConnectAccountServiceServicer
from models.account_connection_models import AccountConnections
from services_caller import account_assistant_service_caller, account_service_caller
from services_caller.account_assistant_service_caller import account_assistant_access_token_caller
from services_caller.account_service_caller import validate_account_services_caller
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

    def ParseAccountMobiles(self, request, context):
        logging.info("ConnectAccountService:ParseAccountMobiles")
        access_done, access_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=access_done, meta_message=access_message)
        if access_done is False:
            return ParseAccountMobilesResponse(response_meta=response_meta)
        else:
            origin_country_code = request.access_auth_details.account.account_country_code
            origin_region_code = phonenumbers.region_code_for_country_code(
                int(origin_country_code.replace('+', '')))
            account_mobiles = []
            for mn in request.connecting_account_mobile_numbers:
                try:
                    parsed_mn = phonenumbers.parse(mn, origin_region_code)
                    account_mobiles.append(AccountMobile(
                        account_country_code="+" + str(parsed_mn.country_code),
                        account_mobile_number=str(parsed_mn.national_number)
                    ))
                except phonenumbers.phonenumberutil.NumberParseException:
                    account_mobiles.append(AccountMobile())
                    logging.warning(f"The {mn} did not seem to be a phone number")
            return ParseAccountMobilesResponse(account_mobiles=account_mobiles, response_meta=response_meta)

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
                    # connect with account assistant
                    _, _, account_assistant_access_auth_details = account_assistant_access_token_caller(
                        access_auth_details=request.access_auth_details)
                    _, _, _ = account_assistant_service_caller.connect_account_caller(
                        access_auth_details=account_assistant_access_auth_details,
                        connecting_account_id=request.connecting_account_id
                    )
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
                # connect with account assistant
                _, _, account_assistant_access_auth_details = account_assistant_access_token_caller(
                    access_auth_details=request.access_auth_details)
                _, _, _ = account_assistant_service_caller.connect_account_caller(
                    access_auth_details=account_assistant_access_auth_details,
                    connecting_account_id=request.connecting_account_id
                )
                # done
                return ConnectAccountResponse(
                    connected_account=connected_account,
                    response_meta=ResponseMeta(meta_done=True, meta_message="Account connected")
                )

    def SyncAccountConnections(self, request, context):
        account_country_code = request.access_auth_details.account.account_country_code
        account_mobile_number = request.access_auth_details.account.account_mobile_number
        if request.connecting_account_mobile.account_mobile_number != account_mobile_number and \
                request.connecting_account_mobile.account_country_code != account_country_code:

            connecting_account = get_account(
                account_mobile_number=request.connecting_account_mobile.account_mobile_number)

            is_account_connected, is_account_connected_message, connected_account = account_service_caller.connect_account_caller(
                access_auth_details=request.access_auth_details,
                connecting_account_id=connecting_account.account_id)

            if is_account_connected:
                yield SyncAccountConnectionsResponse(
                    connected_account=SyncAccountConnectionsResponse.ConnectedAccount(
                        connected_account=connected_account,
                        connected_account_mobile=AccountMobile(
                            account_country_code=request.connecting_account_mobile.account_country_code,
                            account_mobile_number=request.connecting_account_mobile.account_mobile_number
                        )
                    ),
                    response_meta=ResponseMeta(meta_done=is_account_connected,
                                               meta_message=is_account_connected_message)
                )
