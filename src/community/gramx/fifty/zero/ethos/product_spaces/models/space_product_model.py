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

from ethos.elint.entities import space_pb2, space_product_pb2
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

from db_session import DbSession
from support.helper_functions import format_datetime_to_timestamp

BaseModels = declarative_base()


class SpaceProduct(BaseModels):
    __tablename__ = "space_product"

    space_product_id = Column(String(255), primary_key=True, unique=True)
    space_product_name = Column(String(255), nullable=False)
    space_product_admin_account_id = Column(String(255), nullable=False)
    space_id = Column(String(), primary_key=True, nullable=False)
    created_at = Column(DateTime(), nullable=False)


def get_space_product(
    space: space_pb2.Space, with_space_product_id: str = None, with_space_id: str = None
) -> space_product_pb2.SpaceProduct:
    with DbSession.session_scope() as session:
        if with_space_product_id is not None:
            space_product = (
                session.query(SpaceProduct)
                .filter(SpaceProduct.space_product_id == with_space_product_id)
                .first()
            )
        else:
            space_product = (
                session.query(SpaceProduct)
                .filter(SpaceProduct.space_id == with_space_id)
                .first()
            )
        if space_product is None:
            return None
        else:
            # create the space_product obj wrt proto contract
            space_product_obj = space_product_pb2.SpaceProduct(
                space=space,
                space_product_id=space_product.space_product_id,
                space_product_admin_account_id=space_product.space_product_admin_account_id,
                space_product_name=space_product.space_product_name,
                created_at=format_datetime_to_timestamp(space_product.created_at),
            )
            return space_product_obj
