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


from datetime import datetime

from ethos.elint.entities import universe_pb2
from ethos.elint.services.product.identity.universe import create_universe_pb2, update_universe_pb2, delete_universe_pb2

from community.gramx.fifty.zero.ethos.identity.models.base_models import Universe
from db_session import DbSession
from support.helper_functions import format_datetime_to_timestamp, gen_uuid


def get_universe_service(request: create_universe_pb2.CreateUniverseRequest) -> universe_pb2.Universe:
    with DbSession.session_scope() as session:
        universe = session.query(Universe).filter(
            Universe.universe_name == request.universe_name
        ).first()

        universe_obj = universe_pb2.Universe(
            universe_id=universe.universe_id,
            universe_name=universe.universe_name,
            universe_created_at=format_datetime_to_timestamp(universe.universe_created_at),
            universe_description=universe.universe_description,
            universe_updated_at=format_datetime_to_timestamp(universe.universe_updated_at),
        )
    return universe_obj


def create_universe_service(request: create_universe_pb2.CreateUniverseRequest) -> universe_pb2.Universe:
    with DbSession.session_scope() as session:
        # Generate a new universe ID and get the current datetime
        universe_id = gen_uuid()
        created_at = datetime.utcnow()

        # Create a new Universe record
        new_universe = Universe(
            universe_id=universe_id,
            universe_name=request.universe_name,
            universe_created_at=created_at,
            universe_description=request.universe_description,
            universe_updated_at=created_at
        )

        # Add and commit the new universe to the database
        session.add(new_universe)
        session.commit()

        universe_obj = universe_pb2.Universe(
            universe_id=new_universe.universe_id,
            universe_name=new_universe.universe_name,
            universe_created_at=format_datetime_to_timestamp(new_universe.universe_created_at),
            universe_description=new_universe.universe_description,
            universe_updated_at=format_datetime_to_timestamp(new_universe.universe_updated_at)
        )

    return universe_obj


def update_universe_service(request: update_universe_pb2.UpdateUniverseRequest) -> universe_pb2.Universe:
    with DbSession.session_scope() as session:
        # Retrieve the existing Universe record
        universe = session.query(Universe).filter(
            Universe.universe_id == request.universe_id
        ).first()

        if not universe:
            raise ValueError("Universe not found")

        # Update the universe fields
        universe.universe_name = request.universe_name
        universe.universe_description = request.universe_description
        universe.universe_updated_at = datetime.datetime.utcnow()

        # Commit the changes
        session.commit()

        universe_obj = universe_pb2.Universe(
            universe_id=universe.universe_id,
            universe_name=universe.universe_name,
            universe_created_at=format_datetime_to_timestamp(universe.universe_created_at),
            universe_description=universe.universe_description,
            universe_updated_at=format_datetime_to_timestamp(universe.universe_updated_at)
        )

    return universe_obj


def delete_universe_service(request: delete_universe_pb2.DeleteUniverseRequest) -> universe_pb2.Universe:
    with DbSession.session_scope() as session:
        # Retrieve the existing Universe record
        universe = session.query(Universe).filter(
            Universe.universe_id == request.universe_id
        ).first()

        if not universe:
            raise ValueError("Universe not found")

        # Create the universe object to return before deleting
        universe_obj = universe_pb2.Universe(
            universe_id=universe.universe_id,
            universe_name=universe.universe_name,
            universe_created_at=format_datetime_to_timestamp(universe.universe_created_at),
            universe_description=universe.universe_description,
            universe_updated_at=format_datetime_to_timestamp(universe.universe_updated_at)
        )

        # Delete the universe record
        session.delete(universe)
        session.commit()

    return universe_obj
