import os

from sqlalchemy import create_engine

from models import Base

db_url = f"postgres://{os.environ['EA_ID_DB_USER']}" \
         f":{os.environ['EA_ID_DB_PASS']}" \
         f"@{os.environ['EA_ID_DB_HOST']}" \
         f":{os.environ['EA_ID_DB_PORT']}" \
         f"/{os.environ['EA_ID_DB_NAME']}"

engine = create_engine(db_url, echo=True)
# AccountSecrets.__table__.drop(engine)
# AccountConvenienceSecrets.__table__.drop(engine)
# Account.__table__.drop(engine)
Base.metadata.create_all(engine)
