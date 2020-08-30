import grpc

from ethos.elint.entities.account_pb2 import ClaimAccountRequest
from ethos.elint.entities.organization_space_pb2 import ClaimOrganizationSpaceRequest
from ethos.elint.services.product.identity.onboard_account_pb2_grpc import OnboardAccountServiceStub
from ethos.elint.services.product.identity.onboard_organization_space_pb2_grpc import \
    OnboardOrganizationSpaceServiceStub

channel = grpc.insecure_channel('0.0.0.0:50502')

onboard_organization_space_stub = OnboardOrganizationSpaceServiceStub(channel)
result_onboard_organization_space_stub = onboard_organization_space_stub.claim_organization_space(ClaimOrganizationSpaceRequest(
    organization_space_name='space-50g'
))

onboard_account_stub = OnboardAccountServiceStub(channel)
result_onboard_account_stub = onboard_account_stub.claim_account(ClaimAccountRequest(
    account_email_id='amitkumarkhetan15@gmail.com'
))