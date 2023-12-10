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

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

BaseModels = declarative_base()


class SpaceKnowledge(BaseModels):
    __tablename__ = 'space_knowledge'

    space_knowledge_id = Column(String(255), primary_key=True, unique=True)
    space_knowledge_name = Column(String(255), nullable=False)
    space_knowledge_admin_account_id = Column(String(255), nullable=False)
    space_id = Column(String(), primary_key=True, nullable=False)
    created_at = Column(DateTime(), nullable=False)
