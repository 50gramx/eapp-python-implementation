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
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


class DbSession():
    __engine = None
    __session = None

    @staticmethod
    def init_db_session():
        db_url = f"postgresql://{os.environ['EA_ID_DB_USER']}" \
                 f":{os.environ['EA_ID_DB_PASS']}" \
                 f"@{os.environ['EA_ID_DB_HOST']}" \
                 f":{os.environ['EA_ID_DB_PORT']}" \
                 f"/{os.environ['EA_ID_DB_NAME']}"
        DbSession.__engine = create_engine(db_url)
        session_factory = sessionmaker(bind=DbSession.__engine)
        DbSession.__session = scoped_session(session_factory)

    @staticmethod
    @contextmanager
    def session_scope():
        session = DbSession.get_session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def get_engine():
        return DbSession.__engine

    @staticmethod
    def get_session():
        return DbSession.__session()
