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

from ethos.elint.collars import (
    DC499999996_pb2,
    DC499999997_pb2,
    DC499999998_pb2,
    DC499999999_pb2,
    DC500000000_pb2,
)
from ethos.elint.entities import space_service_domain_pb2, space_service_pb2
from sqlalchemy import Boolean, Column, DateTime, String, update

from db_session import DbSession
from src.community.gramx.collars.DC499999998.model import DC499999998Model
from src.community.gramx.collars.DC499999999.model import DC499999999Model
from src.community.gramx.fifty.zero.ethos.service_spaces.models.base import (
    ServiceSpaceModelBase,
)
from support.helper_functions import (
    format_datetime_to_timestamp,
    format_timestamp_to_datetime,
    gen_uuid,
    get_current_timestamp,
)


class ServiceSpace:
    def __init__(self, space_service_id: str):
        self.space_service_id = space_service_id
        self.domain_model_name = f"ssd_{space_service_id}"
        ServiceSpaceModelBase.metadata.reflect(bind=DbSession.get_engine())
        try:
            self.domain_table = ServiceSpaceModelBase.metadata.tables[
                self.domain_model_name
            ]
        except KeyError:
            self.domain_table = None

    # Setup Service Space
    def setup_service_space(self):
        self.get_domain_model().__table__.create(bind=DbSession.get_engine())
        return

    # Domain
    def get_domain_model(self):
        class SpaceServiceDomain(ServiceSpaceModelBase):
            __tablename__ = self.domain_model_name

            id = Column(String(255), primary_key=True, unique=True)
            name = Column(String(255), nullable=False)
            description = Column(String(255), nullable=True)
            collar_code = Column(String(255), nullable=False)
            is_isolated = Column(Boolean(), nullable=False)
            space_service_id = Column(String(255), nullable=False)
            created_at = Column(DateTime(), nullable=False)
            last_updated_at = Column(DateTime(), nullable=False)

        return SpaceServiceDomain

    def get_domain_model_name(self):
        return self.domain_model_name

    def add_new_domain(
        self,
        domain_name: str,
        domain_description: str,
        domain_collar_code: str,
        domain_isolate: bool,
    ) -> str:
        domain_id = gen_uuid()
        statement = (
            ServiceSpaceModelBase.metadata.tables[self.domain_model_name]
            .insert()
            .values(
                id=domain_id,
                name=domain_name,
                description=domain_description,
                collar_code=domain_collar_code,
                is_isolated=domain_isolate,
                space_service_id=self.space_service_id,
                created_at=format_timestamp_to_datetime(get_current_timestamp()),
                last_updated_at=format_timestamp_to_datetime(get_current_timestamp()),
            )
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        # Setup Collar Tables
        if domain_collar_code == "DC499999998":
            domain_service_collar_model = DC499999998Model(
                space_service_domain_id=domain_id,
                space_service_domain_collar_code=domain_collar_code,
            )
            domain_service_collar_model.setup_domain_collar_service_space()
        elif domain_collar_code == "DC499999999":
            domain_service_collar_model = DC499999999Model(
                space_service_domain_id=domain_id,
                space_service_domain_collar_code=domain_collar_code,
            )
            domain_service_collar_model.setup_domain_collar_service_space()
        return domain_id

    def get_domain_with_id(
        self, space_service: space_service_pb2.SpaceService, domain_id: str
    ) -> space_service_domain_pb2.SpaceServiceDomain:
        with DbSession.session_scope() as session:
            if domain_id != "":
                space_service_domain = (
                    session.query(self.domain_table)
                    .filter(self.domain_table.c.id == domain_id)
                    .first()
                )
            if space_service_domain is None:
                return space_service_domain_pb2.SpaceServiceDomain()
            else:
                # TODO: fix domain build based on collar code
                domain = space_service_domain_pb2.SpaceServiceDomain(
                    id=space_service_domain.id,
                    name=space_service_domain.name,
                    description=space_service_domain.description,
                    is_isolated=space_service_domain.is_isolated,
                    space_service=space_service,
                    created_at=format_datetime_to_timestamp(
                        space_service_domain.created_at
                    ),
                    last_updated_at=format_datetime_to_timestamp(
                        space_service_domain.last_updated_at
                    ),
                )
                if space_service_domain.collar_code == "DC499999999":
                    domain_service_collar_model = DC499999999Model(
                        space_service_domain_id=domain_id,
                        space_service_domain_collar_code=space_service_domain.collar_code,
                    )
                    c_proto = domain_service_collar_model.get_collar_proto_latest()
                    domain.dc499999999.CopyFrom(c_proto)
                logging.debug(
                    f"ServiceSpace:get_domain_with_id: {space_service_domain.collar_code}"
                )
                return domain

    def get_domains_with_collar_code(
        self, space_service: space_service_pb2.SpaceService, collar_code: str
    ) -> list:
        with DbSession.session_scope() as session:
            space_service_domains = (
                session.query(self.domain_table)
                .filter_by(self.domain_table.c.collar_code == collar_code)
                .all()
            )

            if not space_service_domains or all(
                domain is None or domain[0] is None for domain in space_service_domains
            ):
                logging.warning("No valid domains found in the domain_table.")
                return []  # Return an empty list if no valid data is found

            return [
                space_service_domain_pb2.SpaceServiceDomain(
                    id=space_service_domain.id,
                    name=space_service_domain.name,
                    description=space_service_domain.description,
                    is_isolated=space_service_domain.is_isolated,
                    space_service=space_service,
                    created_at=format_datetime_to_timestamp(
                        space_service_domain.created_at
                    ),
                    last_updated_at=format_datetime_to_timestamp(
                        space_service_domain.last_updated_at
                    ),
                )
                for space_service_domain in space_service_domains
            ]

    def get_domain_all(self, space_service: space_service_pb2.SpaceService):
        with DbSession.session_scope() as session:
            space_service_domains = session.query(self.domain_table).all()
            if not space_service_domains or all(
                domain is None or domain[0] is None for domain in space_service_domains
            ):
                logging.warning("No valid domains found in the domain_table.")
                return []  # Return an empty list if no valid data is found

            domains = []
            for space_service_domain in space_service_domains:
                domain = space_service_domain_pb2.SpaceServiceDomain(
                    id=space_service_domain.id,
                    name=space_service_domain.name,
                    description=space_service_domain.description,
                    is_isolated=space_service_domain.is_isolated,
                    space_service=space_service,
                    created_at=format_datetime_to_timestamp(
                        space_service_domain.created_at
                    ),
                    last_updated_at=format_datetime_to_timestamp(
                        space_service_domain.last_updated_at
                    ),
                )
                if space_service_domain.collar_code == "DC500000000":
                    domain.dc500000000.CopyFrom(DC500000000_pb2.DC500000000())
                if space_service_domain.collar_code == "DC499999999":
                    cmodel = DC499999999Model(
                        domain.id, space_service_domain.collar_code
                    )
                    domain.dc499999999.CopyFrom(cmodel.get_collar_proto_latest())
                if space_service_domain.collar_code == "DC499999998":
                    domain.dc499999998.CopyFrom(DC499999998_pb2.DC499999998())
                domains.append(domain)
            return domains

    def update_domain_last_updated_at(self, space_service_domain_id: str):
        statement = (
            update(self.domain_table)
            .where(
                self.domain_table.c.space_service_domain_id == space_service_domain_id
            )
            .values(
                last_updated_at=format_timestamp_to_datetime(get_current_timestamp())
            )
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return
