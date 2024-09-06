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

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.exc import IntegrityError
from ethos.identity.models.base_models import Account, Space
from support.helper_functions import format_timestamp_to_datetime, gen_uuid, get_current_timestamp

BaseModels = declarative_base()

class SpaceThings(BaseModels):
    __tablename__ = 'space_things'

    id = Column(String(255), primary_key=True, unique=True)
    name = Column(String(255), nullable=False)
    admin_id = Column(String(255), ForeignKey('account.account_id'), nullable=False)
    space_id = Column(String(255), ForeignKey('space.space_id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=format_timestamp_to_datetime)
    admin = relationship('Account', cascade='save-update', backref='space_things')
    space = relationship('Space', cascade='save-update', backref='space_things')

    def __repr__(self):
        return f"<SpaceThings(id='{self.id}', name='{self.name}', created_at='{self.created_at}')>"

    @classmethod
    def add_new_space_things(cls, session, name, admin_id, space_id):
        """Create a new SpaceThings instance and commit it to the database."""
        try:
            # Create a new SpaceThings instance
            new_space_thing = cls(
                id=gen_uuid(),  # Generate a unique UUID for the new space thing
                name=name,
                admin_id=admin_id,
                space_id=space_id,
                created_at=format_timestamp_to_datetime(get_current_timestamp())
            )
            
            # Add the new instance to the session
            session.add(new_space_thing)
            
            # Commit the session to save the instance to the database
            session.commit()
            
            return new_space_thing.id

        except IntegrityError as e:
            # Rollback the session in case of an error
            session.rollback()
            raise e  # Reraise the exception to handle it at a higher level
        except Exception as e:
            # Handle other potential exceptions
            session.rollback()
            raise e



    
