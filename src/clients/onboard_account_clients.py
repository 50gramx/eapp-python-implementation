import socket

import grpc
from google.protobuf.json_format import MessageToJson

from ethos.elint.entities.organization_space_pb2 import ClaimOrganizationSpaceRequest
from ethos.elint.services.product.identity.onboard_organization_space_pb2_grpc import \
    OnboardOrganizationSpaceServiceStub


host = socket.gethostbyname('https://eapp-identity.herokuapp.com')
port = 14907
channel = grpc.insecure_channel(f"{host}:{port}")

onboard_organization_space_stub = OnboardOrganizationSpaceServiceStub(channel)
result_onboard_organization_space_stub = onboard_organization_space_stub.claim_organization_space(
    ClaimOrganizationSpaceRequest(
        organization_space_name='space-50g'
    ))
print(MessageToJson(result_onboard_organization_space_stub))
print(result_onboard_organization_space_stub.organization_space_available)
#
# onboard_account_stub = OnboardAccountServiceStub(channel)
# result_onboard_account_stub = onboard_account_stub.claim_account(ClaimAccountRequest(
#     account_email_id='amit@techis.io'
# ))
# print(MessageToJson(result_onboard_account_stub))
