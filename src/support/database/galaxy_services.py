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


from ethos.elint.entities import galaxy_pb2
from ethos.elint.entities import universe_pb2
from typing import Tuple
import datetime
from db_session import DbSession
from community.gramx.fifty.zero.ethos.identity.models.base_models import Galaxy
from community.gramx.fifty.zero.ethos.identity.models.base_models import Universe
from support.helper_functions import format_datetime_to_timestamp, gen_uuid


# def get_galaxy(with_galaxy_id: str) -> galaxy_pb2.Galaxy:
#     with DbSession.session_scope() as session:
#         galaxy = session.query(Galaxy).filter(
#             Galaxy.galaxy_id == with_galaxy_id
#         ).first()
#         galaxy_id = galaxy.galaxy_id
#         galaxy_name = galaxy.galaxy_name
#         galaxy_created_at = galaxy.galaxy_created_at
#         universe_id = galaxy.universe_id
#     # create the galaxy obj here wrt proto contract
#     universe = get_universe(with_universe_id=universe_id)
#     galaxy_obj = galaxy_pb2.Galaxy(
#         galaxy_id=galaxy_id,
#         galaxy_name=galaxy_name,
#         universe=universe,
#         galaxy_created_at=format_datetime_to_timestamp(galaxy_created_at)
#     )
#     return galaxy_obj


# def get_our_galaxy() -> galaxy_pb2.Galaxy:
#     with DbSession.session_scope() as session:
#         galaxy = session.query(Galaxy).filter(
#             Galaxy.galaxy_name == "Open Galaxy"
#         ).first()
#         galaxy_id = galaxy.galaxy_id
#         galaxy_name = galaxy.galaxy_name
#         galaxy_created_at = galaxy.galaxy_created_at
#         universe_id = galaxy.universe_id
#     # create the galaxy obj here wrt proto contract
#     universe = get_universe(with_universe_id=universe_id)
#     galaxy_obj = galaxy_pb2.Galaxy(
#         galaxy_id=galaxy_id,
#         galaxy_name=galaxy_name,
#         universe=universe,
#         galaxy_created_at=format_datetime_to_timestamp(galaxy_created_at)
#     )
#     return galaxy_obj

def create_galaxy_service(request: galaxy_pb2.CreateGalaxyRequest) -> galaxy_pb2.Galaxy:
    with DbSession.session_scope() as session:
        # Generate a new galaxy ID and get the current datetime
        galaxy_id = gen_uuid()
        created_at = datetime.datetime.utcnow()

        # Create a new Galaxy record
        new_galaxy = Galaxy(
            galaxy_id=galaxy_id,
            galaxy_name=request.galaxy_name,
            universe_id=request.universe.universe_id,
            domain=request.domain,
            galaxy_description=request.galaxy_description,
            galaxy_created_at=created_at,
            galaxy_updated_at=created_at
        )

        # Add and commit the new galaxy to the database
        session.add(new_galaxy)
        session.commit()

        galaxy_obj = galaxy_pb2.Galaxy(
            galaxy_id=new_galaxy.galaxy_id,
            galaxy_name=new_galaxy.galaxy_name,
            universe=universe_pb2.Universe(
                universe_id=request.universe.universe_id,
                universe_name=request.universe.universe_name,
                universe_created_at=request.universe.universe_created_at,
                universe_description=request.universe.universe_description,
                universe_updated_at=request.universe.universe_updated_at
            ),
            galaxy_created_at=format_datetime_to_timestamp(new_galaxy.galaxy_created_at),
            galaxy_updated_at=format_datetime_to_timestamp(new_galaxy.galaxy_updated_at),
            domain=new_galaxy.domain,
            galaxy_description=new_galaxy.galaxy_description
        )

    return galaxy_obj

def read_galaxy_service(request: galaxy_pb2.ReadGalaxyRequest) -> galaxy_pb2.Galaxy:
    with DbSession.session_scope() as session:
        # Query the Galaxy record
        galaxy = session.query(Galaxy).filter(Galaxy.galaxy_id == request.galaxy_id).first()

        if not galaxy:
            raise ValueError(f"Galaxy with ID {request.galaxy_id} not found")

        # Build the Galaxy protobuf object
        galaxy_obj = galaxy_pb2.Galaxy(
            galaxy_id=galaxy.galaxy_id,
            galaxy_name=galaxy.galaxy_name,
            universe=universe_pb2.Universe(
                universe_id=galaxy.universe.universe_id,
                universe_name=galaxy.universe.universe_name,
                universe_created_at=format_datetime_to_timestamp(galaxy.universe.universe_created_at),
                universe_description=galaxy.universe.universe_description,
                universe_updated_at=format_datetime_to_timestamp(galaxy.universe.universe_updated_at)
            ),
            galaxy_created_at=format_datetime_to_timestamp(galaxy.galaxy_created_at),
            galaxy_updated_at=format_datetime_to_timestamp(galaxy.galaxy_updated_at),
            domain=galaxy.domain,
            galaxy_description=galaxy.galaxy_description
        )

    return galaxy_obj

def update_galaxy_service(request: galaxy_pb2.UpdateGalaxyRequest) -> galaxy_pb2.Galaxy:
    with DbSession.session_scope() as session:
        # Query the existing Galaxy record
        galaxy = session.query(Galaxy).filter(Galaxy.galaxy_id == request.galaxy_id).first()

        if not galaxy:
            raise ValueError(f"Galaxy with ID {request.galaxy_id} not found")

        # Update the Galaxy record
        galaxy.galaxy_name = request.galaxy_name
        galaxy.universe_id = request.universe.universe_id
        galaxy.domain = request.domain
        galaxy.galaxy_description = request.galaxy_description
        galaxy.galaxy_updated_at = datetime.datetime.utcnow()

        # Commit the updates
        session.commit()

        # Build the updated Galaxy protobuf object
        galaxy_obj = galaxy_pb2.Galaxy(
            galaxy_id=galaxy.galaxy_id,
            galaxy_name=galaxy.galaxy_name,
            universe=universe_pb2.Universe(
                universe_id=request.universe.universe_id,
                universe_name=request.universe.universe_name,
                universe_created_at=request.universe.universe_created_at,
                universe_description=request.universe.universe_description,
                universe_updated_at=request.universe.universe_updated_at
            ),
            galaxy_created_at=format_datetime_to_timestamp(galaxy.galaxy_created_at),
            galaxy_updated_at=format_datetime_to_timestamp(galaxy.galaxy_updated_at),
            domain=galaxy.domain,
            galaxy_description=galaxy.galaxy_description
        )

    return galaxy_obj

def delete_galaxy_service(request: galaxy_pb2.DeleteGalaxyRequest) -> Tuple[bool, galaxy_pb2.Galaxy]:
    with DbSession.session_scope() as session:
        # Query the existing Galaxy record
        galaxy = session.query(Galaxy).filter(Galaxy.galaxy_id == request.galaxy_id).first()

        if not galaxy:
            raise ValueError(f"Galaxy with ID {request.galaxy_id} not found")

        # Build the Galaxy protobuf object before deleting
        galaxy_obj = galaxy_pb2.Galaxy(
            galaxy_id=galaxy.galaxy_id,
            galaxy_name=galaxy.galaxy_name,
            universe=universe_pb2.Universe(
                universe_id=galaxy.universe.universe_id,
                universe_name=galaxy.universe.universe_name,
                universe_created_at=format_datetime_to_timestamp(galaxy.universe.universe_created_at),
                universe_description=galaxy.universe.universe_description,
                universe_updated_at=format_datetime_to_timestamp(galaxy.universe.universe_updated_at)
            ),
            galaxy_created_at=format_datetime_to_timestamp(galaxy.galaxy_created_at),
            galaxy_updated_at=format_datetime_to_timestamp(galaxy.galaxy_updated_at),
            domain=galaxy.domain,
            galaxy_description=galaxy.galaxy_description
        )

        # Delete the Galaxy record
        session.delete(galaxy)
        session.commit()

    return True, galaxy_obj