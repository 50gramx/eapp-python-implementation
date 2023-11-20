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

import phonenumbers
from google.protobuf.any_pb2 import Any

from application_context import ApplicationContext
from ethos.elint.entities.account_pb2 import AccountMobile
from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.identity.account.connect_account_pb2 import ConnectedAccountAssistants, \
    ConnectedAccounts, ConnectAccountResponse, ParseAccountMobilesResponse, SyncAccountConnectionsResponse, \
    GetAccountSelfConnectedAccountAssistantResponse, ConnectedAssistantsWithBelongingEntity, \
    IsAccountConnectionExistsRequest, ConnectedAssistantWithBelongingEntity, ConnectedAssistantBelongsTo, \
    GetConnectedAccountResponse, GetConnectedAccountRequest, ParseStreamingAccountMobilesResponse, \
    GetConnectedAccountAssistantResponse, IsAccountAssistantConnectionExistsRequest
from ethos.elint.services.product.identity.account.connect_account_pb2_grpc import ConnectAccountServiceServicer
from ethos.elint.services.product.identity.account.discover_account_pb2 import GetAccountByIdRequest, \
    GetAccountMetaByAccountIdRequest
from ethos.elint.services.product.identity.account_assistant.discover_account_assistant_pb2 import \
    GetAccountAssistantMetaByAccountAssistantIdRequest
from community.gramx.fifty.zero.ethos.identity.models.account_connection_models import AccountConnections
from community.gramx.fifty.zero.ethos.identity.services_caller import account_assistant_service_caller, \
    account_service_caller
from community.gramx.fifty.zero.ethos.identity.services_caller.account_assistant_service_caller import account_assistant_access_token_caller, \
    get_account_assistant_by_account_caller
from community.gramx.fifty.zero.ethos.identity.services_caller.account_service_caller import validate_account_services_caller, \
    account_connected_account_notification_caller
from support.application.tracing import trace_rpc
from support.database.account_services import get_account
from support.helper_functions import gen_uuid


class ConnectAccountService(ConnectAccountServiceServicer):
    def __init__(self):
        super(ConnectAccountService, self).__init__()
        self.session_scope = self.__class__.__name__

    @trace_rpc()
    def GetAccountSelfConnectedAccountAssistant(self, request, context):
        logging.info("ConnectAccountService:GetAccountSelfConnectedAccountAssistant")
        access_done, access_message = validate_account_services_caller(request)
        meta = ResponseMeta(meta_done=access_done, meta_message=access_message)
        if access_done is False:
            return GetAccountSelfConnectedAccountAssistantResponse(response_meta=meta)
        else:
            account_connections = AccountConnections(account_id=request.account.account_id)
            account_assistant_id = get_account_assistant_by_account_caller(account=request.account).account_assistant_id
            connected_account_assistant = account_connections.get_connected_account_assistant(
                account_assistant_id=account_assistant_id)
            return GetAccountSelfConnectedAccountAssistantResponse(
                connected_account_assistant=connected_account_assistant, response_meta=meta)

    @trace_rpc()
    def GetAllConnectedAssistantsWithBelongingEntity(self, request, context):
        logging.info("ConnectAccountService:GetAllConnectedAssistantsWithBelongingEntity")
        # TODO: Remove debugging comments
        access_done, access_message = validate_account_services_caller(request)
        logging.info("validation done")
        meta = ResponseMeta(meta_done=access_done, meta_message=access_message)
        if access_done is False:
            return ConnectedAssistantsWithBelongingEntity(response_meta=meta)
        else:
            logging.info("access is valid")

            # fetching all the params
            logging.info("fetching all connected account assistants")
            all_connected_account_assistant = ApplicationContext.connect_account_service_stub().GetAllConnectedAccountAssistants(
                request).connected_account_assistants
            logging.info(f"fetched all connected account assistants: {all_connected_account_assistant}")

            # yield all the connected_assistant_with_belonging_account
            logging.info("yield all the connected_assistant_with_belonging_account")
            for connected_account_assistant in all_connected_account_assistant:
                logging.info(f"for connected_account_assistant: {connected_account_assistant}")
                account_id = ApplicationContext.discover_account_assistant_service_stub().GetAccountAssistantMetaByAccountAssistantId(
                    GetAccountAssistantMetaByAccountAssistantIdRequest(
                        access_auth_details=request,
                        account_assistant_id=connected_account_assistant.account_assistant_id
                    )).account_assistant_meta.account_id

                is_account_connection_exist = ApplicationContext.connect_account_service_stub().IsAccountConnectionExists(
                    IsAccountConnectionExistsRequest(
                        access_auth_details=request,
                        account_id=None
                    ))
                account = ApplicationContext.discover_account_service_stub().GetAccountById(
                    GetAccountByIdRequest(account_id=account_id)).account
                account_assistant = ApplicationContext.discover_account_assistant_service_stub().GetAccountAssistantByAccount(
                    account)
                any_assistant = Any()
                any_assistant.Pack(account_assistant)
                if is_account_connection_exist:
                    logging.info("return account entity")
                    # return account entity
                    logging.info(f"yielding")
                    any_account = Any()
                    any_account.Pack(account)
                    any_connected_account_assistant = Any()
                    any_connected_account_assistant.Pack(connected_account_assistant)
                    any_connected_entity = Any()
                    connected_account = ApplicationContext.connect_account_service_stub().GetConnectedAccount(
                        GetConnectedAccountRequest(
                            access_auth_details=request,
                            account_id=account_id
                        )).connected_account
                    any_connected_entity.Pack(connected_account)
                    entity = ConnectedAssistantsWithBelongingEntity(
                        connected_assistant_with_belonging_entity=ConnectedAssistantWithBelongingEntity(
                            connected_assistant_belongs_to=ConnectedAssistantBelongsTo.ACCOUNT,
                            connected_assistant=any_connected_account_assistant,
                            assistant=any_assistant,
                            is_connected_to_belonging_entity=True,
                            connected_entity=any_connected_entity,
                            belonging_entity=any_account
                        ),
                        response_meta=meta
                    )
                    logging.info(entity)
                    yield entity
                else:
                    logging.info("return account meta entity")
                    # return account meta entity
                    account_meta = ApplicationContext.discover_account_service_stub().GetAccountMetaByAccountId(
                        GetAccountMetaByAccountIdRequest(
                            access_auth_details=request,
                            account_id=account_id)).account_meta
                    logging.info(f"yielding")
                    any_account_meta = Any()
                    any_account_meta.Pack(account_meta)
                    any_connected_account_assistant = Any()
                    any_connected_account_assistant.Pack(connected_account_assistant)
                    yield ConnectedAssistantsWithBelongingEntity(
                        connected_assistant_with_belonging_entity=ConnectedAssistantWithBelongingEntity(
                            connected_assistant_belongs_to=ConnectedAssistantBelongsTo.ACCOUNT,
                            connected_assistant=any_connected_account_assistant,
                            assistant=any_assistant,
                            is_connected_to_belonging_entity=False,
                            belonging_entity_meta=any_account_meta
                        ),
                        response_meta=meta
                    )
            return ConnectedAssistantsWithBelongingEntity(response_meta=meta)

    @trace_rpc()
    def GetAllConnectedAccountAssistants(self, request, context):
        logging.info("ConnectAccountService:GetAllConnectedAccountAssistants")
        access_done, access_message = validate_account_services_caller(request)
        meta = ResponseMeta(meta_done=access_done, meta_message=access_message)
        if access_done is False:
            return ConnectedAccountAssistants(response_meta=meta)
        else:
            account_connections = AccountConnections(account_id=request.account.account_id)
            self_connected_account_assistant = ApplicationContext.connect_account_service_stub().GetAccountSelfConnectedAccountAssistant(
                request).connected_account_assistant
            list_of_connected_account_assistants = account_connections.get_connected_account_assistants()
            # TODO: remove(self_connected_account_assistant)
            return ConnectedAccountAssistants(
                connected_account_assistants=list_of_connected_account_assistants, response_meta=meta)

    @trace_rpc()
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

    @trace_rpc()
    def GetConnectedAccount(self, request, context):
        logging.info("ConnectAccountService:GetConnectedAccount")
        access_done, access_message = validate_account_services_caller(request.access_auth_details)
        if access_done is False:
            return GetConnectedAccountResponse(
                response_meta=ResponseMeta(meta_done=access_done, meta_message=access_message))
        else:
            is_account_connected = ApplicationContext.connect_account_service_stub().IsAccountConnectionExists(
                IsAccountConnectionExistsRequest(
                    access_auth_details=request.access_auth_details, account_id=request.account_id)).meta_done
            if is_account_connected is False:
                return GetConnectedAccountResponse(
                    response_meta=ResponseMeta(meta_done=False, meta_message="Account not connected."))
            else:
                account_connections = AccountConnections(account_id=request.access_auth_details.account.account_id)
                connected_account = account_connections.get_connected_account(account_id=request.account_id)
                return GetConnectedAccountResponse(
                    connected_account=connected_account,
                    response_meta=ResponseMeta(meta_done=True, meta_message="Account connected."))

    @trace_rpc()
    def GetConnectedAccountAssistant(self, request, context):
        logging.info("ConnectAccountService:GetConnectedAccountAssistant")
        access_done, access_message = validate_account_services_caller(request.access_auth_details)
        if access_done is False:
            return GetConnectedAccountAssistantResponse(
                response_meta=ResponseMeta(meta_done=access_done, meta_message=access_message))
        else:
            is_account_assistant_connected = ApplicationContext.connect_account_service_stub().IsAccountAssistantConnectionExists(
                IsAccountAssistantConnectionExistsRequest(
                    access_auth_details=request.access_auth_details,
                    account_assistant_id=request.account_assistant_id)).meta_done
            if is_account_assistant_connected is False:
                return GetConnectedAccountAssistantResponse(
                    response_meta=ResponseMeta(meta_done=False, meta_message="Account Assistant not connected."))
            else:
                account_connections = AccountConnections(account_id=request.access_auth_details.account.account_id)
                connected_account_assistant = account_connections.get_connected_account_assistant(
                    account_assistant_id=request.account_assistant_id)
                return GetConnectedAccountAssistantResponse(
                    connected_account_assistant=connected_account_assistant,
                    response_meta=ResponseMeta(meta_done=True, meta_message="Account Assistant connected."))

    @trace_rpc()
    def IsAccountConnectionExists(self, request, context):
        logging.info("ConnectAccountService:IsAccountConnectionExists")
        access_done, access_message = validate_account_services_caller(request.access_auth_details)
        if access_done is False:
            return ResponseMeta(meta_done=access_done, meta_message=access_message)
        else:
            account_connections = AccountConnections(account_id=request.access_auth_details.account.account_id)
            is_account_connection_exists = account_connections.is_account_connection_exists(
                account_id=request.account_id)
            return ResponseMeta(meta_done=is_account_connection_exists, meta_message=access_message)

    @trace_rpc()
    def IsAccountAssistantConnectionExists(self, request, context):
        logging.info("ConnectAccountService:IsAccountAssistantConnectionExists")
        access_done, access_message = validate_account_services_caller(request.access_auth_details)
        if access_done is False:
            return ResponseMeta(meta_done=access_done, meta_message=access_message)
        else:
            account_connections = AccountConnections(account_id=request.access_auth_details.account.account_id)
            is_account_assistant_connection_exists = account_connections.is_account_assistant_connection_exists(
                account_assistant_id=request.account_assistant_id)
            return ResponseMeta(meta_done=is_account_assistant_connection_exists, meta_message=access_message)

    @trace_rpc()
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

    @trace_rpc()
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

    @trace_rpc()
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

    @trace_rpc()
    def ParseStreamingAccountMobiles(self, request_iterator, context):
        logging.info("ConnectAccountService:ParseStreamingAccountMobiles")
        origin_country_code = "+91"
        origin_region_code = phonenumbers.region_code_for_country_code(
            int(origin_country_code.replace('+', '')))
        for request in request_iterator:
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
            yield ParseStreamingAccountMobilesResponse(account_mobiles=account_mobiles)

    @trace_rpc()
    def SyncAccountConnections(self, request, context):
        logging.info("ConnectAccountService:SyncAccountConnections")
        access_done, access_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=access_done, meta_message=access_message)
        if access_done is False:
            return SyncAccountConnectionsResponse(response_meta=response_meta)
        else:
            account_mobile_number = request.access_auth_details.account.account_mobile_number
            if request.connecting_account_mobile.account_mobile_number != account_mobile_number:
                connecting_account = get_account(
                    account_mobile_number=request.connecting_account_mobile.account_mobile_number)
                is_account_connected, is_account_connected_message, connected_account = account_service_caller.connect_account_caller(
                    access_auth_details=request.access_auth_details,
                    connecting_account_id=connecting_account.account_id)
                if is_account_connected:
                    return SyncAccountConnectionsResponse(
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
                else:
                    return SyncAccountConnectionsResponse(
                        response_meta=ResponseMeta(meta_done=is_account_connected,
                                                   meta_message=is_account_connected_message)
                    )
            else:
                return SyncAccountConnectionsResponse(
                    response_meta=ResponseMeta(meta_done=False, meta_message="Account Syncing is self account"))

    @trace_rpc()
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
                    # send notification for update
                    _, _ = account_connected_account_notification_caller(
                        account=request.access_auth_details.account,
                        connecting_account_connected_account=connecting_account_connections.get_connected_account(
                            account_id=request.access_auth_details.account.account_id)
                    )
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
                # send notification for update
                _, _ = account_connected_account_notification_caller(
                    account=request.access_auth_details.account,
                    connecting_account_connected_account=connecting_account_connections.get_connected_account(
                        account_id=request.access_auth_details.account.account_id)
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

    @trace_rpc()
    def ToggleAccountConnectAccountInterest(self, request, context):
        logging.info("ConnectAccountService:ToggleAccountConnectAccountInterest")
        access_done, access_message = validate_account_services_caller(request.access_auth_details)
        response_meta = ResponseMeta(meta_done=access_done, meta_message=access_message)
        if access_done is False:
            return response_meta
        else:
            account_connections = AccountConnections(account_id=request.access_auth_details.account.account_id)
            is_account_connection_exists = account_connections.is_account_connection_exists(
                account_id=request.connected_account.account_id)
            if is_account_connection_exists is False:
                return ResponseMeta(meta_done=False,
                                    meta_message="Account not connected. This action will be reported.")
            else:
                connecting_account_connections = AccountConnections(account_id=request.connected_account.account_id)
                if request.connected_account.account_interested_in_connection:
                    # Toggle to not interested
                    account_connections.update_account_interest_in_connection(
                        account_id=request.connected_account.account_id,
                        is_interested=False)
                    connecting_account_connections.update_connected_account_interest_in_connection(
                        account_id=request.access_auth_details.account.account_id, is_interested=False)
                    return response_meta
                else:
                    # Toggle to interested
                    account_connections.update_account_interest_in_connection(
                        account_id=request.connected_account.account_id,
                        is_interested=True)
                    connecting_account_connections.update_connected_account_interest_in_connection(
                        account_id=request.access_auth_details.account.account_id, is_interested=True)
                    return response_meta
