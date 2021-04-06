import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base_models import Base, Universe, Galaxy, Space, AccountConvenienceSecrets, AccountSecrets, Account, \
    AccountDevices, AccountAssistant
from support.helper_functions import gen_uuid, format_timestamp_to_datetime, get_current_timestamp

db_url = f"postgres://{os.environ['EA_ID_DB_USER']}" \
         f":{os.environ['EA_ID_DB_PASS']}" \
         f"@{os.environ['EA_ID_DB_HOST']}" \
         f":{os.environ['EA_ID_DB_PORT']}" \
         f"/{os.environ['EA_ID_DB_NAME']}"

engine = create_engine(db_url, echo=True)

# ----------------------------------
# Delete Tables
# ----------------------------------
Space.__table__.drop(engine)
AccountConvenienceSecrets.__table__.drop(engine)
AccountSecrets.__table__.drop(engine)
AccountDevices.__table__.drop(engine)
AccountAssistant.__table__.drop(engine)
Account.__table__.drop(engine)
Galaxy.__table__.drop(engine)
Universe.__table__.drop(engine)

# ----------------------------------
# Create Tables
# ----------------------------------
Base.metadata.create_all(engine)

# ----------------------------------
# Insert Record in Tables
# ----------------------------------
Session = sessionmaker(bind=engine)
session = Session()
universe_id = gen_uuid()
universe_name = "Ethos Universe"
universe_description = ""
universe_big_bang_at = format_timestamp_to_datetime(get_current_timestamp())

new_universe = Universe(
    universe_id=universe_id,
    universe_name=universe_name,
    universe_description=universe_description,
    universe_big_bang_at=universe_big_bang_at
)
session.add(new_universe)
session.commit()

galaxy_id = gen_uuid()
galaxy_name = "Public Galaxy"
galaxy_created_at = format_timestamp_to_datetime(get_current_timestamp())
universe_id = session.query(Universe).first().universe_id

new_galaxy = Galaxy(
    galaxy_id=galaxy_id,
    galaxy_name=galaxy_name,
    galaxy_created_at=galaxy_created_at,
    universe_id=universe_id
)

session.add(new_galaxy)
session.commit()

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
