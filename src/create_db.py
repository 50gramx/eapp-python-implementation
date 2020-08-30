import os

import datetime
import uuid
from sqlalchemy import Table, Column, String, MetaData, Boolean, ForeignKey, DateTime
from sqlalchemy import create_engine

# db_string = f"postgres://{os.environ['EA_ID_DB_USER']}:{os.environ['EA_ID_DB_PASS']}@{os.environ['EA_ID_DB_HOST']}:{os.environ['EA_ID_DB_PORT']}/{os.environ['EA_ID_DB_NAME']}"
db_string = ""
db = create_engine(db_string)

meta = MetaData(db)

# ForeignKey("organization.organization_id"),
# ALTER TABLE account ADD CONSTRAINT organization_id_fk FOREIGN KEY (organization_id) REFERENCES organization (organization_id);

account_table = Table('account', meta,
                      Column('account_id', String, primary_key=True, unique=True),
                      Column('account_email_id', String, nullable=False, unique=True),
                      Column('first_name', String(40), nullable=False),
                      Column('last_name', String(40), nullable=False),
                      Column('organization_id', String, nullable=False),
                      Column('active', Boolean, nullable=False),
                      Column('admin_acc', Boolean, nullable=False),
                      Column('created_at', DateTime, nullable=False),
                      )

# ForeignKey("org_space.space_id"),
# ALTER TABLE organization ADD CONSTRAINT space_id_fk FOREIGN KEY (organization_space_id) REFERENCES org_space (space_id);

# ForeignKey("account.account_id"),
# ALTER TABLE organization ADD CONSTRAINT account_id_fk FOREIGN KEY (organization_admin_acc_id) REFERENCES account (account_id);

organization_table = Table('organization', meta,
                           Column('organization_id', String, primary_key=True),
                           Column('organization_name', String, nullable=False),
                           Column('organization_space_id', String, nullable=False, unique=True),
                           Column('organization_admin_acc_id', String, nullable=False),
                           Column('active', Boolean, nullable=False),
                           Column('billing_active', Boolean, nullable=False),
                           Column('created_at', DateTime, nullable=False)
                           )


# ForeignKey("knowledge_domain.knowledge_domain_id"),
# ALTER TABLE org_space ADD CONSTRAINT white_knowledge_domain_id_fk FOREIGN KEY (white_knowledge_domain_id) REFERENCES knowledge_domain (knowledge_domain_id);

# ForeignKey("organization.organization_id"),
# ALTER TABLE org_space ADD CONSTRAINT organization_id_fk FOREIGN KEY (organization_id) REFERENCES organization (organization_id);

org_space_table = Table('org_space', meta,
                        Column('space_id', String, primary_key=True),
                        Column('space_name', String, nullable=False, unique=True),
                        Column('white_knowledge_domain_id', String, nullable=False),
                        Column('white_knowledge_domain_name', String, nullable=False),
                        Column('organization_id', String, nullable=False),
                        Column('created_at', DateTime, nullable=False),
                        )

knowledge_domain_table = Table('knowledge_domain', meta,
                               Column('knowledge_domain_id', String, primary_key=True, unique=True),
                               Column('knowledge_domain_name', String, nullable=False),
                               Column('knowledge_domain_description', String),
                               Column('knowledge_domain_color', String, nullable=False),
                               Column('created_at', DateTime, nullable=False),
                               Column('last_updated_at', DateTime, nullable=False)
                               )

with db.connect() as conn:
    # Create
    organization_table.create()
    account_table.create()
    org_space_table.create()
    knowledge_domain_table.create()

    # Create unique ids
    init_acc_id = str(uuid.uuid4())
    init_org_id = str(uuid.uuid4())
    init_space_id = str(uuid.uuid4())
    init_knowledge_domain_id = str(uuid.uuid4())
    print(
        f"init_acc_id: {init_acc_id}, init_org_id: {init_org_id}, space_id: {init_space_id}, kdomain_id: {init_knowledge_domain_id}")

    # Insert
    account_insert_statement = account_table.insert().values(
        account_id=init_acc_id,
        account_email_id='amitkumarkhetan15@gmail.com',
        first_name='Amit',
        last_name='Khetan',
        organization_id=init_org_id,
        active=True,
        admin_acc=True,
        created_at=datetime.datetime.now()
    )
    organization_insert_statement = organization_table.insert().values(
        organization_id=init_org_id,
        organization_name='Ethos',
        organization_space_id=init_space_id,
        organization_admin_acc_id=init_acc_id,
        active=True,
        billing_active=False,
        created_at=datetime.datetime.now()
    )
    org_space_insert_statement = org_space_table.insert().values(
        space_id=init_space_id,
        space_name='space-50g',
        white_knowledge_domain_id=init_knowledge_domain_id,
        white_knowledge_domain_name='white domain',
        organization_id=init_org_id,
        created_at=datetime.datetime.now()
    )

    knowledge_domain_insert_statement = knowledge_domain_table.insert().values(
        knowledge_domain_id=init_knowledge_domain_id,
        knowledge_domain_name='General',
        knowledge_domain_color='white',
        created_at=datetime.datetime.now(),
        last_updated_at=datetime.datetime.now(),
    )

    conn.execute(account_insert_statement)
    conn.execute(organization_insert_statement)
    conn.execute(org_space_insert_statement)
    conn.execute(knowledge_domain_insert_statement)

    # Read
    select_statement = account_table.select()
    result_set = conn.execute(select_statement)
    for r in result_set:
        print(r)

    select_statement = organization_table.select()
    result_set = conn.execute(select_statement)
    for r in result_set:
        print(r)

    select_statement = org_space_table.select()
    result_set = conn.execute(select_statement)
    for r in result_set:
        print(r)

    select_statement = knowledge_domain_table.select()
    result_set = conn.execute(select_statement)
    for r in result_set:
        print(r)

    # Update
    # update_statement = film_table.update().where(film_table.c.year=="2016").values(title = "Some2016Film")
    # conn.execute(update_statement)

    # Delete
    # delete_statement = film_table.delete().where(film_table.c.year == "2016")
    # conn.execute(delete_statement)
