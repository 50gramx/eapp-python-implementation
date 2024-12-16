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

from ethos.elint.entities import space_product_domain_pb2, space_product_pb2
from ethos.elint.services.product.knowledge.space_knowledge.access_space_knowledge_pb2 import (
    SpaceKnowledgeServicesAccessAuthDetails,
)
from sqlalchemy import Boolean, Column, DateTime, String, update

from db_session import DbSession
from src.community.gramx.collars.DC499999994.model import DC499999994Model
from src.community.gramx.fifty.zero.ethos.product_spaces.models.base import (
    ProductSpaceModelBase,
)
from support.helper_functions import (
    format_datetime_to_timestamp,
    format_timestamp_to_datetime,
    gen_uuid,
    get_current_timestamp,
)


class ProductSpace:
    def __init__(self, space_product_id: str):
        self.space_product_id = space_product_id
        self.domain_model_name = f"spd_{space_product_id}"
        ProductSpaceModelBase.metadata.reflect(bind=DbSession.get_engine())
        try:
            self.domain_table = ProductSpaceModelBase.metadata.tables[
                self.domain_model_name
            ]
        except KeyError:
            self.domain_table = None

    # Setup Product Space
    def setup_product_space(self):
        self.get_domain_model().__table__.create(bind=DbSession.get_engine())
        return

    # Domain
    def get_domain_model(self):
        class SpaceProductDomain(ProductSpaceModelBase):
            __tablename__ = self.domain_model_name

            id = Column(String(255), primary_key=True, unique=True)
            name = Column(String(255), nullable=False)
            description = Column(String(255), nullable=True)
            collar_code = Column(String(255), nullable=False)
            is_isolated = Column(Boolean(), nullable=False)
            space_product_id = Column(String(255), nullable=False)
            created_at = Column(DateTime(), nullable=False)
            last_updated_at = Column(DateTime(), nullable=False)

        return SpaceProductDomain

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
            ProductSpaceModelBase.metadata.tables[self.domain_model_name]
            .insert()
            .values(
                id=domain_id,
                name=domain_name,
                description=domain_description,
                collar_code=domain_collar_code,
                is_isolated=domain_isolate,
                space_product_id=self.space_product_id,
                created_at=format_timestamp_to_datetime(get_current_timestamp()),
                last_updated_at=format_timestamp_to_datetime(get_current_timestamp()),
            )
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        # Setup Collar Tables
        if domain_collar_code == "DC499999994":
            domain_service_collar_model = DC499999994Model(
                space_product_domain_id=domain_id,
                space_product_domain_collar_code=domain_collar_code,
            )
            domain_service_collar_model.setup_domain_collar_product_space()
        return domain_id

    def get_domain_with_id(
        self, space_product: space_product_pb2.SpaceProduct, domain_id: str
    ) -> space_product_domain_pb2.SpaceProductDomain:
        with DbSession.session_scope() as session:
            if domain_id != "":
                space_product_domain = (
                    session.query(self.domain_table)
                    .filter(self.domain_table.c.id == domain_id)
                    .first()
                )
            if space_product_domain is None:
                return space_product_domain_pb2.SpaceProductDomain()
            else:
                # TODO: fix domain build based on collar code
                domain = space_product_domain_pb2.SpaceProductDomain(
                    id=space_product_domain.id,
                    name=space_product_domain.name,
                    description=space_product_domain.description,
                    is_isolated=space_product_domain.is_isolated,
                    space_product=space_product,
                    created_at=format_datetime_to_timestamp(
                        space_product_domain.created_at
                    ),
                    last_updated_at=format_datetime_to_timestamp(
                        space_product_domain.last_updated_at
                    ),
                )
                if space_product_domain.collar_code == "DC499999994":
                    domain_product_collar_model = DC499999994Model(
                        space_product_domain_id=domain_id,
                        space_product_domain_collar_code=space_product_domain.collar_code,
                    )
                    c_proto = domain_product_collar_model.get_collar_proto_latest(
                        sk_auth=SpaceKnowledgeServicesAccessAuthDetails(),
                    )
                    domain.dc499999994.CopyFrom(c_proto)
                logging.debug(
                    f"ProductSpace:get_domain_with_id: {space_product_domain.collar_code}"
                )
                return domain

    def get_domains_with_collar_code(
        self, space_product: space_product_pb2.SpaceProduct, collar_code: str
    ):
        with DbSession.session_scope() as session:
            space_product_domains = (
                session.query(self.domain_table)
                .filter_by(self.domain_table.c.collar_code == collar_code)
                .all()
            )

            if not space_product_domains or all(
                domain is None or domain[0] is None for domain in space_product_domains
            ):
                logging.warning("No valid domains found in the domain_table.")
                return []  # Return an empty list if no valid data is found

            return [
                space_product_domain_pb2.SpaceProductDomain(
                    id=space_product_domain.id,
                    name=space_product_domain.name,
                    description=space_product_domain.description,
                    is_isolated=space_product_domain.is_isolated,
                    space_product=space_product,
                    created_at=format_datetime_to_timestamp(
                        space_product_domain.created_at
                    ),
                    last_updated_at=format_datetime_to_timestamp(
                        space_product_domain.last_updated_at
                    ),
                )
                for space_product_domain in space_product_domains
            ]

    def get_domain_all(self, space_product: space_product_pb2.SpaceProduct):
        with DbSession.session_scope() as session:
            space_product_domains = session.query(self.domain_table).all()
            if not space_product_domains or all(
                domain is None or domain[0] is None for domain in space_product_domains
            ):
                logging.warning("No valid domains found in the domain_table.")
                return []  # Return an empty list if no valid data is found

            domains = []
            for space_product_domain in space_product_domains:
                domain = space_product_domain_pb2.SpaceProductDomain(
                    id=space_product_domain.id,
                    name=space_product_domain.name,
                    description=space_product_domain.description,
                    is_isolated=space_product_domain.is_isolated,
                    space_product=space_product,
                    created_at=format_datetime_to_timestamp(
                        space_product_domain.created_at
                    ),
                    last_updated_at=format_datetime_to_timestamp(
                        space_product_domain.last_updated_at
                    ),
                )
                if space_product_domain.collar_code == "DC499999994":
                    domain_product_collar_model = DC499999994Model(
                        space_product_domain_id=space_product_domain.id,
                        space_product_domain_collar_code=space_product_domain.collar_code,
                    )
                    c_proto = domain_product_collar_model.get_collar_proto_latest(
                        sk_auth=SpaceKnowledgeServicesAccessAuthDetails(),
                    )
                    domain.dc499999994.CopyFrom(c_proto)
                domains.append(domain)
            return domains

    def update_domain_last_updated_at(self, space_product_domain_id: str):
        statement = (
            update(self.domain_table)
            .where(
                self.domain_table.c.space_product_domain_id == space_product_domain_id
            )
            .values(
                last_updated_at=format_timestamp_to_datetime(get_current_timestamp())
            )
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return
