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

from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

"""
50GRAMX Chains
"""


class Account(Base):
    __tablename__ = 'account'

    account_analytics_id = Column(String(255), primary_key=True, unique=True)
    account_id = Column(String(255), primary_key=True, unique=True)
    account_personal_email_id = Column(String(255), nullable=True, unique=True)
    account_work_email_id = Column(String(255), nullable=True, unique=True)
    account_country_code = Column(String(6), nullable=False)
    account_mobile_number = Column(String(10), nullable=False, unique=True)
    account_first_name = Column(String(40), nullable=False)
    account_last_name = Column(String(40), nullable=False)
    account_gender = Column(String(10), nullable=False)
    account_birth_at = Column(DateTime(), nullable=False)
    account_galaxy_id = Column(String(255), ForeignKey('galaxy.galaxy_id'), nullable=False)
    account_created_at = Column(DateTime(), nullable=False)
    account_billing_active = Column(Boolean())


class AccountDevices(Base):
    __tablename__ = 'account_devices'

    account_id = Column(String(255), ForeignKey('account.account_id'), primary_key=True)
    account_device_os = Column(Integer(), nullable=False)
    account_device_token = Column(String(255), unique=True, nullable=False)
    account_device_token_accessed_at = Column(DateTime(), nullable=False)


class AccountSecrets(Base):
    __tablename__ = 'account_secrets'

    account_id = Column(String(255), ForeignKey('account.account_id'), primary_key=True, unique=True)
    account_password = Column(String(255), nullable=False)
    account_password_last_updated_geo_lat = Column(String(255), nullable=False)
    account_password_last_updated_geo_long = Column(String(255), nullable=False)
    account_password_last_updated_at = Column(DateTime())
    account_password_created_at = Column(DateTime(), nullable=False)


class AccountConvenienceSecrets(Base):
    __tablename__ = 'account_convenience_secrets'

    account_id = Column(String(255), ForeignKey('account.account_id'), primary_key=True, unique=True)
    account_convenience_pin = Column(String(6), nullable=False)
    account_convenience_pin_created_at = Column(DateTime(), nullable=False)


class Universe(Base):
    __tablename__ = "universe"

    universe_id = Column(String(255), primary_key=True, unique=True)
    universe_name = Column(String(255), nullable=False, unique=True)
    universe_description = Column(String(255), nullable=False)
    universe_created_at = Column(DateTime(), nullable=False)
    universe_updated_at = Column(DateTime())


class Galaxy(Base):
    __tablename__ = "galaxy"

    galaxy_id = Column(String(255), primary_key=True, unique=True)
    galaxy_name = Column(String(255), nullable=False)
    universe_id = Column(String(255), ForeignKey('universe.universe_id'), nullable=False)
    galaxy_created_at = Column(DateTime(), nullable=False)


class Space(Base):
    __tablename__ = "space"

    space_id = Column(String(255), primary_key=True, unique=True)
    space_admin_id = Column(String(255), ForeignKey('account.account_id'))
    galaxy_id = Column(String(255), ForeignKey('galaxy.galaxy_id'), nullable=False)
    space_accessibility_type = Column(String(), nullable=False)
    space_isolation_type = Column(String(), nullable=False)
    space_entity_type = Column(String(), nullable=False)
    space_created_at = Column(DateTime(), nullable=False)


class AccountAssistant(Base):
    __tablename__ = "account_assistant"

    account_assistant_id = Column(String(255), primary_key=True)
    account_assistant_name_code = Column(Integer(), nullable=False)
    account_assistant_name = Column(String(255), nullable=False)
    account_id = Column(String(255), ForeignKey('account.account_id'))
    created_at = Column(DateTime(), nullable=False)
    last_assisted_at = Column(DateTime(), nullable=False)


class AccountAssistantNameCode(Base):
    __tablename__ = "account_assistant_name_code"

    account_assistant_name = Column(String(255), primary_key=True)
    account_assistant_name_code = Column(Integer(), primary_key=True)
    account_id = Column(String(255), primary_key=True)


class CoreCollaborator(Base):
    __tablename__ = "core_collaborator"

    collaborator_first_name = Column(String(255), primary_key=True)
    collaborator_last_name = Column(String(255), primary_key=True)
    collaborator_community_code = Column(Integer(), primary_key=True)
