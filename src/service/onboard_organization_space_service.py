import logging

import grpc
from sqlalchemy import exists
from sqlalchemy.exc import SQLAlchemyError

from db_session import DbSession
from ethos.elint.entities.organization_space_pb2 import ClaimOrganizationSpaceResponse
from ethos.elint.services.product.identity.organisation.onboard_organization_space_pb2_grpc import \
    OnboardOrganizationSpaceServiceServicer

from models.organization_space_model import OrgSpace

logger = logging.getLogger(__name__)


class OnboardOrganizationSpaceService(OnboardOrganizationSpaceServiceServicer):
    pass
    # def claim_organization_space(self, request, context):
    #     organization_available = False
    #     # Check the claimed space name in db
    #     if request.organization_space_name is not None:
    #         try:
    #             with DbSession.session_scope() as session:
    #                 filter_statement = exists().where(OrgSpace.space_name == request.organization_space_name)
    #                 result_set = session.query(OrgSpace).filter(filter_statement)
    #                 session.commit()
    #         except SQLAlchemyError as err:
    #             logger.error("SQLAlchemyError {}".format(str(err)))
    #             context.set_code(grpc.StatusCode.UNKNOWN)
    #         # Generate the boolean feedback about the availability
    #         for record in result_set:
    #             if record.space_name == request.organization_space_name:
    #                 organization_available = False
    #             else:
    #                 organization_available = True
    #     # Return the response
    #     return ClaimOrganizationSpaceResponse(
    #         organization_space_available=organization_available,
    #         message=""
    #     )
