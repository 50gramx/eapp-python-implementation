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
from ethos.identity.models.base_models import Account, Space
from support.helper_functions import format_timestamp_to_datetime

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

    
