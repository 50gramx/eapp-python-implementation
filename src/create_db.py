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

import os

from sqlalchemy import create_engine

from models.base_models import Base
from models.pay_in_models import PayIn

db_url = f"postgres://{os.environ['EA_ID_DB_USER']}" \
         f":{os.environ['EA_ID_DB_PASS']}" \
         f"@{os.environ['EA_ID_DB_HOST']}" \
         f":{os.environ['EA_ID_DB_PORT']}" \
         f"/{os.environ['EA_ID_DB_NAME']}"

engine = create_engine(db_url, echo=True)

# ----------------------------------
# Delete Tables
# ----------------------------------
# AccountAssistantNameCode.__table__.drop(engine)
# Space.__table__.drop(engine)
# AccountConvenienceSecrets.__table__.drop(engine)
# AccountSecrets.__table__.drop(engine)
# AccountDevices.__table__.drop(engine)
# AccountAssistant.__table__.drop(engine)
# Account.__table__.drop(engine)
# Galaxy.__table__.drop(engine)
# Universe.__table__.drop(engine)

# ----------------------------------
# Create Tables
# ----------------------------------
Base.metadata.create_all(engine)
PayIn.metadata.create_all(engine)

# ----------------------------------
# Insert Record in Tables
# ----------------------------------
# Session = sessionmaker(bind=engine)
# session = Session()
#
# account_pay_in = AccountPayIn(
#     account_id="0CEBA68E-1351-418E-BFD1-30765445AA0D",
#     account_pay_id="cus_JMniakQgJAv6nP"
# )
# session.add(account_pay_in)
# session.commit()

# universe_id = gen_uuid()
# universe_name = "Ethos Universe"
# universe_description = ""
# universe_big_bang_at = format_timestamp_to_datetime(get_current_timestamp())
#
# new_universe = Universe(
#     universe_id=universe_id,
#     universe_name=universe_name,
#     universe_description=universe_description,
#     universe_big_bang_at=universe_big_bang_at
# )
# session.add(new_universe)
# session.commit()

# galaxy_id = gen_uuid()
# galaxy_name = "Public Galaxy"
# galaxy_created_at = format_timestamp_to_datetime(get_current_timestamp())
# universe_id = session.query(Universe).first().universe_id
#
# new_galaxy = Galaxy(
#     galaxy_id=galaxy_id,
#     galaxy_name=galaxy_name,
#     galaxy_created_at=galaxy_created_at,
#     universe_id=universe_id
# )
#
# session.add(new_galaxy)
# session.commit()

# ----------------------------------
# Delete Record in Tables
# ----------------------------------
# Session = sessionmaker(bind=engine)
# session = Session()
#
# account = session.query(Space).first()
# session.delete(account)
#
# session.commit()

#
# db_session.DbSession.init_db_session()
# # create assistant name code
# account_assistant_name_code = get_account_assistant_name_code(
#     account_assistant_name="Chiku")
# new_account_assistant_id = add_new_account_assistant(
#     account_id="6C71095B-3631-494A-A754-413B5ADD980F",
#     account_assistant_name_code=account_assistant_name_code,
#     account_assistant_name="Chiku")
# account_assistant_connections = AccountAssistantConnections(account_assistant_id=new_account_assistant_id)
# account_assistant_connections.setup_account_assistant_connections()
#
# account_connections = AccountConnections(account_id="6C71095B-3631-494A-A754-413B5ADD980F")
# new_connection_id = gen_uuid()
# account_assistant_connections.add_new_account_connection(
#     account_connection_id=new_connection_id,
#     account_id="6C71095B-3631-494A-A754-413B5ADD980F")
# account_connections.add_new_account_assistant_connection(
#     account_assistant_connection_id=new_connection_id,
#     account_assistant_id=new_account_assistant_id
# )
#
# account_assistant_connections = AccountAssistantConnections(account_assistant_id="63CC78F0-AE0B-4CC4-9ACE-1405B0F5C4FD")
# is_account_connection_exists = account_assistant_connections.is_account_connected(
#     account_id="0CEBA68E-1351-418E-BFD1-30765445AA0D")
# new_connection_id = gen_uuid()
# connecting_account_connections = AccountConnections(account_id="0CEBA68E-1351-418E-BFD1-30765445AA0D")
# account_assistant_connections.add_new_account_connection(
#     account_connection_id=new_connection_id,
#     account_id="0CEBA68E-1351-418E-BFD1-30765445AA0D"
# )
# connecting_account_connections.add_new_account_assistant_connection(
#     account_assistant_connection_id=new_connection_id,
#     account_assistant_id="63CC78F0-AE0B-4CC4-9ACE-1405B0F5C4FD"
# )
