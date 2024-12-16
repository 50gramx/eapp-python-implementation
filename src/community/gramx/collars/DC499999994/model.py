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

import ethos.elint.collars.DC499999994_pb2 as cpb2
from ethos.elint.services.product.knowledge.space_knowledge.access_space_knowledge_pb2 import (
    SpaceKnowledgeServicesAccessAuthDetails,
)
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db_session import DbSession
from src.community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge.discover.consumers.discover_space_knowledge_consumer import (
    DiscoverSpaceKnowledgeConsumer,
)
from src.community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.discover.consumers.discover_space_knowledge_domain_consumer import (
    DiscoverSpaceKnowledgeDomainConsumer,
)
from src.community.gramx.fifty.zero.ethos.knowledge_spaces.models.knowledge_space_models import (
    KnowledgeSpace,
)
from src.community.gramx.fifty.zero.ethos.product_spaces.models.base import (
    ProductSpaceModelBase,
)
from src.support.helper_functions import (
    format_datetime_to_timestamp,
    format_timestamp_to_datetime,
    gen_uuid,
    get_current_timestamp,
)

# TODO(Anyone): Add README.md + Code Documentations & Comments


class DC499999994Model:
    def __init__(
        self,
        space_product_domain_id: str,
        space_product_domain_collar_code: str,
    ):
        self.domain_id = space_product_domain_id
        self.domain_collar_code = space_product_domain_collar_code

        self.skincare_product_model_name = self._get_table_name(code=5000)
        self.images_model_name = self._get_table_name(code=5022)
        self.collar_model_name = self._get_table_name(code=9999)
        try:
            self.collar_table = ProductSpaceModelBase.metadata.tables[
                self.collar_model_name
            ]
            self.skincare_product_table = ProductSpaceModelBase.metadata.tables[
                self.skincare_product_model_name
            ]
            self.images_table = ProductSpaceModelBase.metadata.tables[
                self.images_model_name
            ]
        except Exception as e:
            logging.info(f"DC499999994Model: init, KeyError: {e}")
            self.collar_table = None
            self.skincare_product_table = None
            self.images_table = None

    def _get_table_name(self, code: int) -> str:
        return f"{self.domain_collar_code}_{code}_{self.domain_id}"

    # Setup Domain Service Space
    def setup_domain_collar_product_space(self):
        self.get_skincare_product_model().__table__.create(bind=DbSession.get_engine())
        # SkincareProduct Entities
        self.get_images_model().__table__.create(bind=DbSession.get_engine())
        # Collar Entities
        self.get_DC499999994_collar_model().__table__.create(
            bind=DbSession.get_engine()
        )
        return

    def get_DC499999994_collar_model(self):
        class DC499999994(ProductSpaceModelBase):
            __tablename__ = self.collar_model_name

            id = Column(String, primary_key=True, unique=True)
            name = Column(String(255), nullable=False)
            description = Column(String)

            # One-to-One relationship with SkincareProduct
            skincare_product_id = Column(
                String, ForeignKey(f"{self.skincare_product_model_name}.id")
            )
            skincare_product = relationship(
                "SkincareProduct",
                back_populates=f"{self.collar_model_name}",
                uselist=False,
            )

            images_sk_id = Column(String, nullable=False)
            images_skd_id = Column(String, nullable=False)
            created_at = Column(DateTime(), nullable=False)
            updated_at = Column(DateTime(), nullable=False)

        return DC499999994

    def get_collar(
        self, id: str, sk_auth: SpaceKnowledgeServicesAccessAuthDetails
    ) -> cpb2.DC499999994:
        with DbSession.session_scope() as session:
            collar = (
                session.query(self.collar_table)
                .filter(self.collar_table.c.id == id)
                .first()
            )
            (
                md,
                mm,
                product_images_domain,
            ) = DiscoverSpaceKnowledgeConsumer().get_space_knowledge_domain_by_id(
                access_auth_details=sk_auth,
                space_knowledge_domain_id=collar.images_skd_id,
            )
            logging.info(
                f"DC499999994Model, get_collar, product_images_domain: {product_images_domain}, {md}, {mm}"
            )
            return cpb2.DC499999994(
                id=collar.id,
                name=collar.name,
                description=collar.description,
                skincare_product=self.get_skincare_product_proto(
                    collar.skincare_product_id
                ),
                product_images_domain=product_images_domain,
                created_at=format_datetime_to_timestamp(collar.created_at),
                updated_at=format_datetime_to_timestamp(collar.created_at),
            )

    def get_collar_proto_latest(
        self, sk_auth: SpaceKnowledgeServicesAccessAuthDetails
    ) -> cpb2.DC499999994:
        with DbSession.session_scope() as session:
            logging.info(f"get_collar_proto_latest: {type(self.collar_table)}")
            collar = session.query(self.collar_table).first()
            if collar is None:
                return cpb2.DC499999994()
            try:
                return self.get_collar(id=collar.id, sk_auth=sk_auth)
            except Exception as e:
                logging.exception(f"get_collar_proto_latest: {e}")
                return cpb2.DC499999994()

    def get_collar_all(self) -> list:
        with DbSession.session_scope() as session:
            collars = session.query(self.collar_table).all()
            collars_proto = []
            for collar in collars:
                try:
                    collars_proto.append(
                        cpb2.DC499999994(
                            id=collar.id,
                            name=collar.name,
                            description=collar.description,
                            skincare_product=self.get_skincare_product_proto(
                                collar.skincare_product_id
                            ),
                            created_at=format_datetime_to_timestamp(collar.created_at),
                            updated_at=format_datetime_to_timestamp(collar.created_at),
                        )
                    )
                except Exception as e:
                    logging.info(f"collar,e: {collar}, {e}")
            return collars_proto

    def add_collar(
        self,
        skincare_product_id: str,
        name: str = "",
        description: str = "",
        images_sk_id: str = "",
        images_skd_id: str = "",
    ) -> str:
        """Add skincare_product data from a protobuf object into the database."""

        # reserve new id
        id = gen_uuid()

        # add collar record statement
        statement = (
            ProductSpaceModelBase.metadata.tables[self.collar_model_name]
            .insert()
            .values(
                id=id,
                name=name,
                description=description,
                skincare_product_id=skincare_product_id,
                images_sk_id=images_sk_id,
                images_skd_id=images_skd_id,
                created_at=format_timestamp_to_datetime(get_current_timestamp()),
                updated_at=format_timestamp_to_datetime(get_current_timestamp()),
            )
        )

        # Commit to save all changes
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()

        # Pass collar id
        return id

    def get_skincare_product_model(self):
        class SkincareProduct(ProductSpaceModelBase):
            __tablename__ = self.skincare_product_model_name

            id = Column(String, primary_key=True)
            name = Column(String, nullable=False)

            # TODO: fix unused params
            # One-to-One Relationships
            skincare_product_images = relationship(
                "SkincareProductImages",
                uselist=False,
                back_populates=self.skincare_product_model_name,
            )  # Used

        return SkincareProduct

    def add_skincare_product_from_proto(
        self, skincare_product_proto: cpb2.SkincareProduct
    ) -> str:
        """Add skincare_product data from a protobuf object into the database."""

        # reserve new id
        id = gen_uuid()

        # add skincare_product record statement
        statement = (
            ProductSpaceModelBase.metadata.tables[self.skincare_product_model_name]
            .insert()
            .values(
                id=id,
                name=skincare_product_proto.name,
            )
        )

        # Commit to save all changes
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()

        # Add related entities like metadata, labels, and annotations
        # TODO: for rest params
        if skincare_product_proto.HasField("images"):
            self._add_product_images_from_proto(skincare_product_proto.images, id)

        # Pass skincare_product id
        return id

    def get_skincare_product_proto(self, skincare_product_id) -> cpb2.SkincareProduct:
        with DbSession.session_scope() as session:
            # Fetch skincare_product record from the database
            logging.info(
                f"self.skincare_product_table: {self.skincare_product_table}, {type(self.skincare_product_table)}"
            )
            skincare_product = (
                session.query(self.skincare_product_table)
                .filter(self.skincare_product_table.c.id == skincare_product_id)
                .first()
            )
            if not skincare_product:
                raise ValueError(
                    f"SkincareProduct with ID {skincare_product_id} not found"
                )

            # Fetch related pod template, replica config, etc., if needed
            logging.info(
                f"self.images_table: {self.images_table}, {type(self.images_table)}"
            )
            images = (
                session.query(self.images_table)
                .filter(self.images_table.c.product_id == skincare_product_id)
                .first()
            )

            # Handle missing pod template or replica config
            if not images:
                logging.warning("not skincare_product_image")
                images = cpb2.ProductImages()

            images = cpb2.ProductImages(
                id=f"{images.id}",
                product_id=skincare_product_id,
            )

            # Construct the SkincareProduct proto
            skincare_product_proto = cpb2.SkincareProduct(
                id=skincare_product_id,
                name=f"{skincare_product.name}",
                images=images,
                # createdAt=format_datetime_to_timestamp(skincare_product.created_at),
                # updatedAt=format_datetime_to_timestamp(skincare_product.updated_at),
            )

            return skincare_product_proto

    def get_images_model(self):
        class ProductImages(ProductSpaceModelBase):
            __tablename__ = self.images_model_name

            id = Column(Integer, primary_key=True, autoincrement=True)
            product_id = Column(
                String, ForeignKey(f"{self.skincare_product_model_name}.id")
            )
            primary_image = Column(String, nullable=False)
            packaging_image = Column(String, nullable=False)
            logistics_image = Column(String, nullable=False)

            # Many-to-One relationship with SkincareProduct
            skincare_product = relationship(
                "SkincareProduct", back_populates=self.skincare_product_model_name
            )

        return ProductImages

    def _add_product_images_from_proto(
        self, pt: cpb2.ProductImages, skincare_product_id: str
    ):
        with DbSession.session_scope() as session:
            pt_statement = (
                ProductSpaceModelBase.metadata.tables[self.images_model_name]
                .insert()
                .values(
                    product_id=skincare_product_id,
                )
                .returning(
                    ProductSpaceModelBase.metadata.tables[self.images_model_name].c.id
                )
            )
            result = session.execute(pt_statement)
            pt_id = result.scalar()  # Retrieve the auto-assigned ID
            session.commit()
        return pt_id
