from datetime import datetime

from db_session import DbSession
from ethos.elint.entities import account_pb2, galaxy_pb2, universe_pb2, space_pb2, account_assistant_pb2
from ethos.elint.entities.account_assistant_pb2 import AccountAssistantMeta
from ethos.elint.entities.space_pb2 import SpaceAccessibilityType, SpaceIsolationType, SpaceEntityType
from models.base_models import Account, Space, Galaxy, Universe, AccountAssistant, AccountDevices, \
    AccountAssistantNameCode
from support.format_proto_entities import format_account_assistant_to_entity
from support.helper_functions import gen_uuid, get_current_timestamp, \
    format_timestamp_to_datetime, format_datetime_to_timestamp


def is_existing_account_email(account_email_id: str) -> bool:
    """
    checks for the existence of account_email_id in account table as a personal_email_id
    :param account_email_id:
    :return:
    """
    with DbSession.session_scope() as session:
        q = session.query(Account.account_id).filter(
            Account.account_personal_email_id == account_email_id
        )
        account_exists = session.query(q.exists()).scalar()
    return account_exists


def is_existing_account_mobile(account_country_code: str, account_mobile_number: str) -> bool:
    """
    check for the existence of account_mobile_number in account table as a account_mobile_number
    :param account_country_code:
    :param account_mobile_number:
    :return:
    """
    with DbSession.session_scope() as session:
        q = session.query(Account.account_id).filter(
            Account.account_country_code == account_country_code,
            Account.account_mobile_number == account_mobile_number
        )
        account_exists = session.query(q.exists()).scalar()
        return account_exists


def get_account_assistant_name_code(account_assistant_name: str) -> int:
    account_assistant_name = account_assistant_name.lower()
    with DbSession.session_scope() as session:
        account_assistant_name_code = session.query(AccountAssistantNameCode).filter(
            AccountAssistantNameCode.account_assistant_name == account_assistant_name
        ).all()
        if len(account_assistant_name_code) > 0:
            new_name_code = len(account_assistant_name_code) + 1
        else:
            new_name_code = 1
        session.add(AccountAssistantNameCode(account_assistant_name=account_assistant_name,
                                             account_assistant_name_code=new_name_code))
        session.commit()
        return new_name_code


def add_new_account(account: Account) -> None:
    with DbSession.session_scope() as session:
        session.add(account)
        session.commit()
    return


def add_new_space(space: Space) -> None:
    with DbSession.session_scope() as session:
        session.add(space)
        session.commit()
    return


def add_new_account_devices(account_devices: AccountDevices) -> None:
    with DbSession.session_scope() as session:
        session.add(account_devices)
        session.commit()
    return


def update_account_devices(account_id: str, account_device_os: int, account_device_token: str,
                           account_device_token_accessed_at: datetime) -> None:
    with DbSession.session_scope() as session:
        existing_account_devices = session.query(AccountDevices).filter(
            AccountDevices.account_id == account_id
        ).first()
        existing_account_devices.account_device_os = account_device_os
        existing_account_devices.account_device_token = account_device_token
        existing_account_devices.account_device_token_accessed_at = account_device_token_accessed_at
        session.commit()
    return


def add_new_entity(entity) -> None:
    """
    Adds a new record in the database table of specified entity
    :param entity: an entity of Base Class (base_models.py)
    :return: None
    """
    with DbSession.session_scope() as session:
        session.add(entity)
        session.commit()
    return


def add_new_account_assistant(account_id: str, account_assistant_name_code: int, account_assistant_name: str) -> str:
    created_at = get_current_timestamp()
    last_assisted_at = get_current_timestamp()
    account_assistant_id = gen_uuid()
    new_account_assistant = AccountAssistant(
        account_assistant_id=account_assistant_id,
        account_assistant_name_code=account_assistant_name_code,
        account_assistant_name=account_assistant_name,
        account_id=account_id,
        created_at=format_timestamp_to_datetime(created_at),
        last_assisted_at=format_timestamp_to_datetime(last_assisted_at)
    )
    add_new_entity(new_account_assistant)
    return account_assistant_id


def get_universe(with_universe_id: str) -> universe_pb2.Universe:
    with DbSession.session_scope() as session:
        universe = session.query(Universe).filter(
            Universe.universe_id == with_universe_id
        ).first()
        # create the universe obj here wrt proto contract
        universe_obj = universe_pb2.Universe(
            universe_id=universe.universe_id,
            big_bang_at=format_datetime_to_timestamp(universe.universe_big_bang_at),
            universe_name=universe.universe_name,
            universe_description=universe.universe_description
        )
    return universe_obj


def get_galaxy(with_galaxy_id: str) -> galaxy_pb2.Galaxy:
    with DbSession.session_scope() as session:
        galaxy = session.query(Galaxy).filter(
            Galaxy.galaxy_id == with_galaxy_id
        ).first()
        galaxy_id = galaxy.galaxy_id
        galaxy_name = galaxy.galaxy_name
        galaxy_created_at = galaxy.galaxy_created_at
        universe_id = galaxy.universe_id
    # create the galaxy obj here wrt proto contract
    universe = get_universe(with_universe_id=universe_id)
    galaxy_obj = galaxy_pb2.Galaxy(
        galaxy_id=galaxy_id,
        galaxy_name=galaxy_name,
        universe=universe,
        galaxy_created_at=format_datetime_to_timestamp(galaxy_created_at)
    )
    return galaxy_obj


def get_our_galaxy() -> galaxy_pb2.Galaxy:
    with DbSession.session_scope() as session:
        galaxy = session.query(Galaxy).filter(
            Galaxy.galaxy_name == "Public Galaxy"
        ).first()
        galaxy_id = galaxy.galaxy_id
        galaxy_name = galaxy.galaxy_name
        galaxy_created_at = galaxy.galaxy_created_at
        universe_id = galaxy.universe_id
    # create the galaxy obj here wrt proto contract
    universe = get_universe(with_universe_id=universe_id)
    galaxy_obj = galaxy_pb2.Galaxy(
        galaxy_id=galaxy_id,
        galaxy_name=galaxy_name,
        universe=universe,
        galaxy_created_at=format_datetime_to_timestamp(galaxy_created_at)
    )
    return galaxy_obj


def get_account(account_id: str = None, account_mobile_number: str = None) -> account_pb2.Account:
    with DbSession.session_scope() as session:
        if account_id is not None:
            account = session.query(Account).filter(
                Account.account_id == account_id
            ).first()
        else:
            account = session.query(Account).filter(
                Account.account_mobile_number == account_mobile_number
            ).first()
        # create the account obj here wrt proto contract
        account_obj = account_pb2.Account(
            account_analytics_id=account.account_analytics_id,
            account_id=account.account_id,
            account_personal_email_id=account.account_personal_email_id,
            account_work_email_id=account.account_work_email_id,
            account_country_code=account.account_country_code,
            account_mobile_number=account.account_mobile_number,
            account_first_name=account.account_first_name,
            account_last_name=account.account_last_name,
            account_galaxy_id=account.account_galaxy_id,
            account_birth_at=format_datetime_to_timestamp(account.account_birth_at),
            account_gender=account_pb2.AccountGender.Name(int(account.account_gender)),
            created_at=format_datetime_to_timestamp(account.account_created_at),
            account_billing_active=str(account.account_billing_active)
        )
    return account_obj


def get_space(with_space_id: str = None, with_account_id: str = None) -> space_pb2.Space:
    with DbSession.session_scope() as session:
        if with_space_id is not None:
            space = session.query(Space).filter(
                Space.space_id == with_space_id
            ).first()
        else:
            space = session.query(Space).filter(
                Space.space_admin_id == with_account_id
            ).first()
        if space is None:
            return None
        galaxy_id = space.galaxy_id
        space_id = space.space_id
        space_accessibility_type = space.space_accessibility_type
        space_isolation_type = space.space_isolation_type
        space_entity_type = space.space_entity_type
        space_admin_id = space.space_admin_id
        space_created_at = space.space_created_at
    # create the space obj wrt proto contract
    space_obj = space_pb2.Space(
        space_id=space_id,
        galaxy=get_galaxy(with_galaxy_id=galaxy_id),
        space_accessibility_type=SpaceAccessibilityType.Name(int(space_accessibility_type)),
        space_isolation_type=SpaceIsolationType.Name(int(space_isolation_type)),
        space_entity_type=SpaceEntityType.Name(int(space_entity_type)),
        space_admin_id=space_admin_id,
        space_created_at=format_datetime_to_timestamp(space_created_at)
    )
    return space_obj


def get_account_assistant(account: account_pb2.Account) -> account_assistant_pb2.AccountAssistant:
    with DbSession.session_scope() as session:
        account_assistant = session.query(AccountAssistant).filter(
            AccountAssistant.account_id == account.account_id
        ).first()
        return format_account_assistant_to_entity(
            account=account,
            account_assistant=account_assistant,
            session=session
        )


def get_account_assistant_meta(account_id: str = None, account_assistant_id: str = None) -> AccountAssistantMeta:
    with DbSession.session_scope() as session:
        if account_id is not None:
            account_assistant = session.query(AccountAssistant).filter(
                AccountAssistant.account_id == account_id
            ).first()
        else:
            account_assistant = session.query(AccountAssistant).filter(
                AccountAssistant.account_assistant_id == account_assistant_id
            ).first()
        return AccountAssistantMeta(
            account_assistant_id=account_assistant.account_assistant_id,
            account_assistant_name_code=account_assistant.account_assistant_name_code,
            account_assistant_name=account_assistant.account_assistant_name,
            account_id=account_assistant.account_id
        )


def get_account_device_token(account_id: str) -> str:
    with DbSession.session_scope() as session:
        account_device = session.query(AccountDevices).filter(
            AccountDevices.account_id == account_id
        ).first()
        return account_device.account_device_token
