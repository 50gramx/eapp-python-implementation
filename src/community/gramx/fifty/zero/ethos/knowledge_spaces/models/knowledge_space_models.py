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

import logging
import unicodedata

from ethos.elint.entities import (
    space_knowledge_domain_file_page_para_pb2,
    space_knowledge_domain_file_page_pb2,
    space_knowledge_domain_file_pb2,
    space_knowledge_domain_pb2,
    space_knowledge_pb2,
)
from ethos.elint.entities.space_knowledge_domain_file_page_para_pb2 import (
    PageContourDimensions,
)
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, update
from sqlalchemy.ext.declarative import declarative_base

from db_session import DbSession
from support.helper_functions import (
    format_datetime_to_timestamp,
    format_timestamp_to_datetime,
    gen_uuid,
    get_current_timestamp,
)

KnowledgeSpaceModels = declarative_base()


class KnowledgeSpace:
    def __init__(self, space_knowledge_id: str):
        self.space_knowledge_id = space_knowledge_id
        self.domain_model_name = f"skd_{space_knowledge_id}"
        self.inferred_domain_model_name = f"skid_{space_knowledge_id}"
        KnowledgeSpaceModels.metadata.reflect(bind=DbSession.get_engine())
        try:
            self.domain_table = KnowledgeSpaceModels.metadata.tables[
                self.domain_model_name
            ]
            self.inferred_domain_table = KnowledgeSpaceModels.metadata.tables[
                self.inferred_domain_model_name
            ]
        except KeyError:
            self.domain_table = None
            self.inferred_domain_table = None

    # Setup Knowledge Space
    def setup_knowledge_space(self):
        self.get_domain_model().__table__.create(bind=DbSession.get_engine())
        self.get_inferred_domain_model().__table__.create(bind=DbSession.get_engine())
        return

    # Domain
    def get_domain_model(self):
        class SpaceKnowledgeDomain(KnowledgeSpaceModels):
            __tablename__ = self.domain_model_name

            space_knowledge_domain_id = Column(
                String(255), primary_key=True, unique=True
            )
            space_knowledge_domain_name = Column(String(255), nullable=False)
            space_knowledge_domain_description = Column(String(255), nullable=True)
            space_knowledge_domain_collar_enum = Column(Integer, nullable=False)
            space_knowledge_domain_isolated = Column(Boolean(), nullable=False)
            space_knowledge_id = Column(String(255), nullable=False)
            created_at = Column(DateTime(), nullable=False)
            last_updated_at = Column(DateTime(), nullable=False)

        return SpaceKnowledgeDomain

    def get_domain_model_name(self):
        return self.domain_model_name

    def add_new_domain(
        self,
        domain_name: str,
        domain_description: str,
        domain_collar_enum: int,
        domain_isolate: bool,
    ) -> str:
        domain_id = gen_uuid()
        statement = (
            KnowledgeSpaceModels.metadata.tables[self.domain_model_name]
            .insert()
            .values(
                space_knowledge_domain_id=domain_id,
                space_knowledge_domain_name=domain_name,
                space_knowledge_domain_description=domain_description,
                space_knowledge_domain_collar_enum=domain_collar_enum,
                space_knowledge_domain_isolated=domain_isolate,
                space_knowledge_id=self.space_knowledge_id,
                created_at=format_timestamp_to_datetime(get_current_timestamp()),
                last_updated_at=format_timestamp_to_datetime(get_current_timestamp()),
            )
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        domain_knowledge_space = DomainKnowledgeSpace(
            space_knowledge_id=self.space_knowledge_id,
            space_knowledge_domain_id=domain_id,
        )
        domain_knowledge_space.setup_domain_knowledge_space()
        return domain_id

    def get_domain_with_id(
        self, space_knowledge: space_knowledge_pb2.SpaceKnowledge, domain_id: str
    ) -> space_knowledge_domain_pb2.SpaceKnowledgeDomain:
        with DbSession.session_scope() as session:
            if domain_id != "":
                space_knowledge_domain = (
                    session.query(self.domain_table)
                    .filter(self.domain_table.c.space_knowledge_domain_id == domain_id)
                    .first()
                )
            else:
                space_knowledge_domain = (
                    session.query(self.domain_table)
                    .filter(self.domain_table.c.space_knowledge_domain_collar_enum == 0)
                    .first()
                )
            if space_knowledge_domain is None:
                return space_knowledge_domain_pb2.SpaceKnowledgeDomain()
            else:
                return space_knowledge_domain_pb2.SpaceKnowledgeDomain(
                    space_knowledge_domain_id=space_knowledge_domain.space_knowledge_domain_id,
                    space_knowledge_domain_name=space_knowledge_domain.space_knowledge_domain_name,
                    space_knowledge_domain_description=space_knowledge_domain.space_knowledge_domain_description,
                    space_knowledge_domain_collar_enum=space_knowledge_domain_pb2.SpaceKnowledgeDomainCollarEnum.Name(
                        int(space_knowledge_domain.space_knowledge_domain_collar_enum)
                    ),
                    space_knowledge_domain_isolated=space_knowledge_domain.space_knowledge_domain_isolated,
                    space_knowledge=space_knowledge,
                    created_at=format_datetime_to_timestamp(
                        space_knowledge_domain.created_at
                    ),
                    last_updated_at=format_datetime_to_timestamp(
                        space_knowledge_domain.last_updated_at
                    ),
                )

    def get_domain_all(self, space_knowledge: space_knowledge_pb2.SpaceKnowledge):
        with DbSession.session_scope() as session:
            space_knowledge_domains = session.query(self.domain_table).all()
            if not space_knowledge_domains or all(
                domain is None or domain[0] is None
                for domain in space_knowledge_domains
            ):
                logging.warning("No valid domains found in the domain_table.")
                return []  # Return an empty list if no valid data is found

            logging.info(
                f"KnowledgeSpace:get_domain_all:space_knowledge_domains:{space_knowledge_domains}"
            )
            return [
                space_knowledge_domain_pb2.SpaceKnowledgeDomain(
                    space_knowledge_domain_id=space_knowledge_domain.space_knowledge_domain_id,
                    space_knowledge_domain_name=space_knowledge_domain.space_knowledge_domain_name,
                    space_knowledge_domain_description=space_knowledge_domain.space_knowledge_domain_description,
                    space_knowledge_domain_collar_enum=space_knowledge_domain_pb2.SpaceKnowledgeDomainCollarEnum.Name(
                        int(space_knowledge_domain.space_knowledge_domain_collar_enum)
                    ),
                    space_knowledge_domain_isolated=space_knowledge_domain.space_knowledge_domain_isolated,
                    space_knowledge=space_knowledge,
                    created_at=format_datetime_to_timestamp(
                        space_knowledge_domain.created_at
                    ),
                    last_updated_at=format_datetime_to_timestamp(
                        space_knowledge_domain.last_updated_at
                    ),
                )
                for space_knowledge_domain in space_knowledge_domains
            ]

    def update_domain_last_updated_at(self, space_knowledge_domain_id: str):
        statement = (
            update(self.domain_table)
            .where(
                self.domain_table.c.space_knowledge_domain_id
                == space_knowledge_domain_id
            )
            .values(
                last_updated_at=format_timestamp_to_datetime(get_current_timestamp())
            )
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return

    # Inferred Domain
    def get_inferred_domain_model(self):
        class SpaceKnowledgeInferredDomain(KnowledgeSpaceModels):
            __tablename__ = self.inferred_domain_model_name

            inferred_domain_id = Column(String(255), primary_key=True)
            space_knowledge_id = Column(String(255), nullable=False)
            space_knowledge_domain_id = Column(String(255), primary_key=True)
            inferred_at = Column(DateTime, nullable=False)

        return SpaceKnowledgeInferredDomain

    def get_inferred_domain_model_name(self):
        return self.inferred_domain_model_name

    def add_new_inferred_domain(
        self,
        inferred_domain_id: str,
        space_knowledge_id: str,
        space_knowledge_domain_id: str,
    ):
        statement = (
            KnowledgeSpaceModels.metadata.tables[self.inferred_domain_model_name]
            .insert()
            .values(
                inferred_domain_id=inferred_domain_id,
                space_knowledge_id=space_knowledge_id,
                space_knowledge_domain_id=space_knowledge_domain_id,
                inferred_at=format_timestamp_to_datetime(get_current_timestamp()),
            )
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return

    def is_existing_inferred_domain(
        self,
        inferred_domain_id: str,
        space_knowledge_id: str,
        space_knowledge_domain_id: str,
    ) -> bool:
        with DbSession.session_scope() as session:
            statement = session.query(self.inferred_domain_table).filter(
                self.inferred_domain_table.c.inferred_domain_id == inferred_domain_id,
                self.inferred_domain_table.c.space_knowledge_id == space_knowledge_id,
                self.inferred_domain_table.c.space_knowledge_domain_id
                == space_knowledge_domain_id,
            )
            inferred_domain_exists = session.query(statement.exists()).scalar()
            return inferred_domain_exists

    def get_inferred_domain_all(self):
        with DbSession.session_scope() as session:
            all_space_knowledge_domain_inferred = session.query(
                self.inferred_domain_table
            ).all()
            return [
                space_knowledge_domain_pb2.SpaceKnowledgeDomainInferred(
                    inferred_domain_id=space_knowledge_domain_inferred.inferred_domain_id,
                    space_knowledge_id=space_knowledge_domain_inferred.space_knowledge_id,
                    space_knowledge_domain_id=space_knowledge_domain_inferred.space_knowledge_domain_id,
                    inferred_at=format_datetime_to_timestamp(
                        space_knowledge_domain_inferred.inferred_at
                    ),
                )
                for space_knowledge_domain_inferred in all_space_knowledge_domain_inferred
            ]


class DomainKnowledgeSpace:
    def __init__(self, space_knowledge_id: str, space_knowledge_domain_id: str):
        self.space_knowledge_domain_id = space_knowledge_domain_id
        self.domain_model_name = KnowledgeSpace(
            space_knowledge_id=space_knowledge_id
        ).get_domain_model_name()
        self.inferring_account_model_name = f"ia_{space_knowledge_domain_id}"
        self.file_model_name = f"skdf_{space_knowledge_domain_id}"
        self.file_tags_model_name = f"skdft_{space_knowledge_domain_id}"
        self.file_tags_relations_model_name = f"skdftr_{space_knowledge_domain_id}"
        self.page_model_name = f"skdfp_{space_knowledge_domain_id}"
        self.page_text_model_name = f"skdfpt_{space_knowledge_domain_id}"
        self.para_model_name = f"skdfpp_{space_knowledge_domain_id}"
        self.para_text_model_name = f"skdfppt_{space_knowledge_domain_id}"
        self.domain_qa_context_model_name = f"qa_context_{space_knowledge_domain_id}"
        KnowledgeSpaceModels.metadata.reflect(bind=DbSession.get_engine())
        try:
            self.file_table = KnowledgeSpaceModels.metadata.tables[self.file_model_name]
            self.file_tags_table = KnowledgeSpaceModels.metadata.tables[
                self.file_tags_model_name
            ]
            self.file_tags_relations_table = KnowledgeSpaceModels.metadata.tables[
                self.file_tags_relations_model_name
            ]
            self.page_table = KnowledgeSpaceModels.metadata.tables[self.page_model_name]
            self.page_text_table = KnowledgeSpaceModels.metadata.tables[
                self.page_text_model_name
            ]
            self.para_table = KnowledgeSpaceModels.metadata.tables[self.para_model_name]
            self.para_text_table = KnowledgeSpaceModels.metadata.tables[
                self.para_text_model_name
            ]
            self.domain_qa_context_table = KnowledgeSpaceModels.metadata.tables[
                self.domain_qa_context_model_name
            ]
        except KeyError:
            self.file_table = None
            self.file_tags_table = None
            self.file_tags_relations_table = None
            self.page_table = None
            self.page_text_table = None
            self.para_table = None
            self.para_text_table = None
            self.domain_qa_context_table = None

    # Setup Domain Knowledge Space
    def setup_domain_knowledge_space(self):
        self.get_inferring_account_model().__table__.create(bind=DbSession.get_engine())
        self.get_file_model().__table__.create(bind=DbSession.get_engine())
        self.get_file_tags_model().__table__.create(bind=DbSession.get_engine())
        self.get_file_tags_relations_model().__table__.create(
            bind=DbSession.get_engine()
        )
        self.get_page_model().__table__.create(bind=DbSession.get_engine())
        self.get_page_text_model().__table__.create(bind=DbSession.get_engine())
        self.get_para_model().__table__.create(bind=DbSession.get_engine())
        self.get_para_text_model().__table__.create(bind=DbSession.get_engine())
        self.get_domain_qa_context_model().__table__.create(bind=DbSession.get_engine())
        return

    # Inferring Accounts
    def get_inferring_account_model(self):
        class SpaceKnowledgeDomainInferringAccount(KnowledgeSpaceModels):
            __tablename__ = self.inferring_account_model_name

            inferring_account_id = Column(String(255), primary_key=True)
            space_knowledge_id = Column(String(255), nullable=False)
            account_id = Column(String(255), primary_key=True)
            inferred_at = Column(DateTime, nullable=False)

        return SpaceKnowledgeDomainInferringAccount

    def get_inferring_account_model_name(self):
        return self.inferring_account_model_name

    def add_new_inferring_account(
        self, inferring_account_id: str, space_knowledge_id: str, account_id: str
    ):
        statement = (
            KnowledgeSpaceModels.metadata.tables[self.inferring_account_model_name]
            .insert()
            .values(
                inferring_account_id=inferring_account_id,
                space_knowledge_id=space_knowledge_id,
                account_id=account_id,
                inferred_at=format_timestamp_to_datetime(get_current_timestamp()),
            )
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return

        # File

    # File
    def get_file_model(self):
        class SpaceKnowledgeDomainFile(KnowledgeSpaceModels):
            __tablename__ = self.file_model_name

            space_knowledge_domain_file_id = Column(
                String(255), primary_key=True, unique=True
            )
            space_knowledge_domain_file_name = Column(String(255), nullable=False)
            space_knowledge_domain_file_size = Column(Integer(), nullable=False)
            space_knowledge_domain_file_extension_type = Column(
                Integer(), nullable=False
            )
            space_knowledge_domain_id = Column(
                String(255),
                ForeignKey(f"{self.domain_model_name}.space_knowledge_domain_id"),
                nullable=False,
            )
            created_at = Column(DateTime(), nullable=False)
            last_updated_at = Column(DateTime(), nullable=False)
            last_accessed_at = Column(DateTime(), nullable=False)

        return SpaceKnowledgeDomainFile

    def get_file_model_name(self):
        return self.file_model_name

    def add_new_file(
        self, file_name: str, file_extension_type: str, file_size: int
    ) -> str:
        file_id = gen_uuid()
        statement = (
            KnowledgeSpaceModels.metadata.tables[self.file_model_name]
            .insert()
            .values(
                space_knowledge_domain_file_id=file_id,
                space_knowledge_domain_file_name=file_name,
                space_knowledge_domain_file_extension_type=file_extension_type,
                space_knowledge_domain_file_size=file_size,
                space_knowledge_domain_id=self.space_knowledge_domain_id,
                created_at=format_timestamp_to_datetime(get_current_timestamp()),
                last_updated_at=format_timestamp_to_datetime(get_current_timestamp()),
                last_accessed_at=format_timestamp_to_datetime(get_current_timestamp()),
            )
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return file_id

    def get_file_with_id(
        self,
        space_knowledge_domain: space_knowledge_domain_pb2.SpaceKnowledgeDomain,
        file_id: str,
    ) -> space_knowledge_domain_file_pb2.SpaceKnowledgeDomainFile:
        with DbSession.session_scope() as session:
            space_knowledge_domain_file = (
                session.query(self.file_table)
                .filter(self.file_table.c.space_knowledge_domain_file_id == file_id)
                .first()
            )
            space_knowledge_domain_file_tags = self.get_file_tags(
                file_id=space_knowledge_domain_file.space_knowledge_domain_file_id
            )
            return space_knowledge_domain_file_pb2.SpaceKnowledgeDomainFile(
                space_knowledge_domain_file_id=space_knowledge_domain_file.space_knowledge_domain_file_id,
                space_knowledge_domain_file_name=space_knowledge_domain_file.space_knowledge_domain_file_name,
                space_knowledge_domain_file_size=space_knowledge_domain_file.space_knowledge_domain_file_size,
                space_knowledge_domain_file_extension_type=space_knowledge_domain_file_pb2.ExtentionType.Name(
                    int(
                        space_knowledge_domain_file.space_knowledge_domain_file_extension_type
                    )
                ),
                space_knowledge_domain=space_knowledge_domain,
                space_knowledge_domain_file_tags=space_knowledge_domain_file_tags,
                created_at=format_datetime_to_timestamp(
                    space_knowledge_domain_file.created_at
                ),
                last_updated_at=format_datetime_to_timestamp(
                    space_knowledge_domain_file.last_updated_at
                ),
                last_accessed_at=format_datetime_to_timestamp(
                    space_knowledge_domain_file.last_accessed_at
                ),
            )

    def get_file_all_existing(
        self, space_knowledge_domain: space_knowledge_domain_pb2.SpaceKnowledgeDomain
    ) -> [space_knowledge_domain_file_pb2.SpaceKnowledgeDomainFile]:
        with DbSession.session_scope() as session:
            space_knowledge_domain_files = session.query(self.file_table).all()
            # create the space_knowledge_domain_file obj wrt proto contract
            list_of_space_knowledge_domain_file = list()
            for space_knowledge_domain_file in space_knowledge_domain_files:
                space_knowledge_domain_file_tags = self.get_file_tags(
                    file_id=space_knowledge_domain_file.space_knowledge_domain_file_id
                )
                list_of_space_knowledge_domain_file.append(
                    space_knowledge_domain_file_pb2.SpaceKnowledgeDomainFile(
                        space_knowledge_domain_file_id=space_knowledge_domain_file.space_knowledge_domain_file_id,
                        space_knowledge_domain_file_name=space_knowledge_domain_file.space_knowledge_domain_file_name,
                        space_knowledge_domain_file_size=space_knowledge_domain_file.space_knowledge_domain_file_size,
                        space_knowledge_domain_file_extension_type=space_knowledge_domain_file_pb2.ExtentionType.Name(
                            int(
                                space_knowledge_domain_file.space_knowledge_domain_file_extension_type
                            )
                        ),
                        space_knowledge_domain=space_knowledge_domain,
                        space_knowledge_domain_file_tags=space_knowledge_domain_file_tags,
                        created_at=format_datetime_to_timestamp(
                            space_knowledge_domain_file.created_at
                        ),
                        last_updated_at=format_datetime_to_timestamp(
                            space_knowledge_domain_file.last_updated_at
                        ),
                        last_accessed_at=format_datetime_to_timestamp(
                            space_knowledge_domain_file.last_accessed_at
                        ),
                    )
                )
            return list_of_space_knowledge_domain_file

    def delete_file_by_id(self, file_id: str):
        with DbSession.session_scope() as session:
            file = (
                session.query(self.file_table)
                .filter(self.file_table.c.space_knowledge_domain_file_id == file_id)
                .delete(synchronize_session=False)
            )
            # session.delete(file)
            session.commit()

    def get_file_count(self) -> int:
        with DbSession.session_scope() as session:
            file_count = session.query(self.file_table).count()
            return file_count

    # File Tags
    def get_file_tags_model(self):
        class FileTags(KnowledgeSpaceModels):
            __tablename__ = self.file_tags_model_name

            file_tag_id = Column(String(), primary_key=True)
            file_tag_name = Column(String(), nullable=False)

        return FileTags

    def get_file_tags_name(self):
        return self.file_tags_model_name

    # File Tags Relations
    def get_file_tags_relations_model(self):
        class FileTagsRelations(KnowledgeSpaceModels):
            __tablename__ = self.file_tags_relations_model_name

            file_tags_relations_id = Column(
                Integer(), autoincrement=True, primary_key=True
            )
            space_knowledge_domain_file_id = Column(
                String(255),
                ForeignKey(f"{self.file_model_name}.space_knowledge_domain_file_id"),
            )
            space_knowledge_domain_file_tag_id = Column(
                String(), ForeignKey(f"{self.file_tags_model_name}.file_tag_id")
            )

        return FileTagsRelations

    def get_file_tags_relations_model_name(self):
        return self.file_tags_relations_model_name

    def get_file_tags(self, file_id: str) -> [space_knowledge_domain_file_pb2.FileTag]:
        with DbSession.session_scope() as session:
            # get all the tag ids from FileTagsRelations
            file_tag_ids = (
                session.query(
                    self.file_tags_relations_table.c.space_knowledge_domain_file_tag_id
                )
                .filter(
                    self.file_tags_relations_table.c.space_knowledge_domain_file_id
                    == file_id
                )
                .all()
            )
            # get all tag names from FileTags for respective file_tag_id
            file_tags = session.query(
                self.file_tags_table.c.file_tag_id, self.file_tags_table.c.file_tag_name
            ).filter(self.file_tags_table.c.file_tag_id.in_(file_tag_ids))
            # create list of space_knowledge_domain_file_pb2.FileTag
            list_of_file_tag = [
                space_knowledge_domain_file_pb2.FileTag(
                    file_tag_id=file_tag.file_tag_id,
                    file_tag_name=file_tag.file_tag_name,
                )
                for file_tag in file_tags
            ]
        return list_of_file_tag

    # Page
    def get_page_model(self):
        class SpaceKnowledgeDomainFilePage(KnowledgeSpaceModels):
            __tablename__ = self.page_model_name

            space_knowledge_domain_file_page_id = Column(
                String(255), primary_key=True, unique=True
            )
            space_knowledge_domain_file_page_count = Column(Integer, nullable=False)
            space_knowledge_domain_file_id = Column(
                String(255),
                ForeignKey(f"{self.file_model_name}.space_knowledge_domain_file_id"),
                nullable=False,
            )
            created_at = Column(DateTime(), nullable=False)
            last_updated_at = Column(DateTime(), nullable=False)
            last_accessed_at = Column(DateTime(), nullable=False)

        return SpaceKnowledgeDomainFilePage

    def get_page_model_name(self):
        return self.page_model_name

    def add_new_page(self, page_count: int, file_id: str) -> str:
        page_id = gen_uuid()
        statement = (
            KnowledgeSpaceModels.metadata.tables[self.page_model_name]
            .insert()
            .values(
                space_knowledge_domain_file_page_id=page_id,
                space_knowledge_domain_file_page_count=page_count,
                space_knowledge_domain_file_id=file_id,
                created_at=format_timestamp_to_datetime(get_current_timestamp()),
                last_updated_at=format_timestamp_to_datetime(get_current_timestamp()),
                last_accessed_at=format_timestamp_to_datetime(get_current_timestamp()),
            )
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return page_id

    def get_page_with_id(
        self,
        space_knowledge_domain_file: space_knowledge_domain_file_pb2.SpaceKnowledgeDomainFile,
        page_id: str,
    ) -> space_knowledge_domain_file_page_pb2.SpaceKnowledgeDomainFilePage:
        with DbSession.session_scope() as session:
            space_knowledge_domain_file_page = (
                session.query(self.page_table)
                .filter(
                    self.page_table.c.space_knowledge_domain_file_page_id == page_id
                )
                .first()
            )
            return space_knowledge_domain_file_page_pb2.SpaceKnowledgeDomainFilePage(
                space_knowledge_domain_file_page_id=space_knowledge_domain_file_page.space_knowledge_domain_file_page_id,
                space_knowledge_domain_file_page_count=space_knowledge_domain_file_page.space_knowledge_domain_file_page_count,
                space_knowledge_domain_file=space_knowledge_domain_file,
                created_at=format_datetime_to_timestamp(
                    space_knowledge_domain_file_page.created_at
                ),
                last_updated_at=format_datetime_to_timestamp(
                    space_knowledge_domain_file_page.last_updated_at
                ),
                last_accessed_at=format_datetime_to_timestamp(
                    space_knowledge_domain_file_page.last_accessed_at
                ),
            )

    def get_page_count(self) -> int:
        with DbSession.session_scope() as session:
            page_count = session.query(self.page_table).count()
            return page_count

    def get_file_id_with_page_id(self, page_id: str):
        with DbSession.session_scope() as session:
            space_knowledge_domain_file_page = (
                session.query(self.page_table)
                .filter(
                    self.page_table.c.space_knowledge_domain_file_page_id == page_id
                )
                .first()
            )
            return space_knowledge_domain_file_page.space_knowledge_domain_file_id

    def get_all_page_id_with_file_id(self, file_id: str) -> [str]:
        with DbSession.session_scope() as session:
            space_knowledge_domain_file_pages = (
                session.query(self.page_table)
                .filter(self.page_table.c.space_knowledge_domain_file_id == file_id)
                .all()
            )
            list_of_page_ids = list()
            for space_knowledge_domain_file_page in space_knowledge_domain_file_pages:
                list_of_page_ids.append(
                    space_knowledge_domain_file_page.space_knowledge_domain_file_page_id
                )
            return list_of_page_ids

    def delete_page_by_id(self, page_id: str):
        with DbSession.session_scope() as session:
            page = (
                session.query(self.page_table)
                .filter(
                    self.page_table.c.space_knowledge_domain_file_page_id == page_id
                )
                .delete(synchronize_session=False)
            )
            # session.delete(page)
            session.commit()

    # TODO: Add tags models

    # Page Text
    def get_page_text_model(self):
        class SpaceKnowledgeDomainPageText(KnowledgeSpaceModels):
            __tablename__ = self.page_text_model_name

            page_id = Column(
                String,
                ForeignKey(
                    f"{self.page_model_name}.space_knowledge_domain_file_page_id"
                ),
                primary_key=True,
            )
            page_text = Column("page_text", String)

        return SpaceKnowledgeDomainPageText

    def get_page_text_model_name(self):
        return self.page_text_model_name

    def add_new_page_text(self, page_id: str, page_text: str):
        KnowledgeSpaceModels.metadata.reflect(bind=DbSession.get_engine())
        statement = (
            KnowledgeSpaceModels.metadata.tables[self.page_text_model_name]
            .insert()
            .values(page_id=page_id, page_text=page_text)
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()

    def get_page_text_all_id(self):
        with DbSession.session_scope() as session:
            page_text_ids = session.query(self.page_text_table.c.page_id).all()
            list_of_page_text_ids = list()
            for page_text_id in page_text_ids:
                list_of_page_text_ids.append(page_text_id)
            return list_of_page_text_ids

    def get_page_text_by_id(self, page_id: str):
        with DbSession.session_scope() as session:
            page_text = (
                session.query(self.page_text_table.c.page_text)
                .filter(self.page_text_table.c.page_id == page_id)
                .first()
            )
            return unicodedata.normalize("NFD", str(page_text))

    def delete_page_text_by_id(self, page_id: str):
        with DbSession.session_scope() as session:
            page_text = (
                session.query(self.page_text_table)
                .filter(self.page_text_table.c.page_id == page_id)
                .delete(synchronize_session=False)
            )
            # session.delete(page_text)
            session.commit()
        return

    # Para
    def get_para_model(self):
        class SpaceKnowledgeDomainFilePagePara(KnowledgeSpaceModels):
            __tablename__ = self.para_model_name

            space_knowledge_domain_file_page_para_id = Column(
                String(255), primary_key=True, unique=True
            )
            space_knowledge_domain_file_page_id = Column(
                String(255),
                ForeignKey(
                    f"{self.page_model_name}.space_knowledge_domain_file_page_id"
                ),
                nullable=False,
            )
            page_contour_dimensions = Column(String, nullable=False)
            created_at = Column(DateTime(), nullable=False)
            last_updated_at = Column(DateTime(), nullable=False)
            last_accessed_at = Column(DateTime(), nullable=False)

        return SpaceKnowledgeDomainFilePagePara

    def get_para_model_name(self):
        return self.para_model_name

    def add_new_para(self, page_id: str, contour_dims: dict):
        para_id = gen_uuid()
        contour_dimensions = (
            f"{contour_dims.get('x', 0)}:"
            f"{contour_dims.get('y', 0)}:"
            f"{contour_dims.get('w', 0)}:"
            f"{contour_dims.get('h', 0)}"
        )
        statement = (
            KnowledgeSpaceModels.metadata.tables[self.para_model_name]
            .insert()
            .values(
                space_knowledge_domain_file_page_para_id=para_id,
                space_knowledge_domain_file_page_id=page_id,
                page_contour_dimensions=contour_dimensions,
                created_at=format_timestamp_to_datetime(get_current_timestamp()),
                last_updated_at=format_timestamp_to_datetime(get_current_timestamp()),
                last_accessed_at=format_timestamp_to_datetime(get_current_timestamp()),
            )
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return para_id

    def get_para_with_id(
        self,
        para_id: str,
        space_knowledge_domain_file_page: space_knowledge_domain_file_page_pb2.SpaceKnowledgeDomainFilePage,
    ):
        with DbSession.session_scope() as session:
            space_knowledge_domain_file_page_para = (
                session.query(self.para_table)
                .filter(
                    self.para_table.c.space_knowledge_domain_file_page_para_id
                    == para_id
                )
                .first()
            )
            dims_list = str(
                space_knowledge_domain_file_page_para.page_contour_dimensions
            ).split(":")
            logging.info(
                f"object types:: x:{type(dims_list[0])}, y:{type(dims_list[1])}, w:{type(dims_list[2])}, h:{type(dims_list[3])}"
            )
            logging.info(
                f"object values:: x:{dims_list[0]}, y:{dims_list[1]}, w:{dims_list[2]}, h:{dims_list[3]}"
            )
            page_contour_dims = PageContourDimensions(
                x=int(float(dims_list[0])),
                y=int(float(dims_list[1])),
                w=int(float(dims_list[2])),
                h=int(float(dims_list[3])),
            )
            return space_knowledge_domain_file_page_para_pb2.SpaceKnowledgeDomainFilePagePara(
                space_knowledge_domain_file_page_para_id=space_knowledge_domain_file_page_para.space_knowledge_domain_file_page_para_id,
                space_knowledge_domain_file_page=space_knowledge_domain_file_page,
                page_contour_dimensions=page_contour_dims,
                created_at=format_datetime_to_timestamp(
                    space_knowledge_domain_file_page_para.created_at
                ),
                last_updated_at=format_datetime_to_timestamp(
                    space_knowledge_domain_file_page_para.last_updated_at
                ),
                last_accessed_at=format_datetime_to_timestamp(
                    space_knowledge_domain_file_page_para.last_accessed_at
                ),
            )

    def get_page_id_with_para_id(self, para_id: str):
        with DbSession.session_scope() as session:
            space_knowledge_domain_file_page_para = (
                session.query(self.para_table)
                .filter(
                    self.para_table.c.space_knowledge_domain_file_page_para_id
                    == para_id
                )
                .first()
            )
            return (
                space_knowledge_domain_file_page_para.space_knowledge_domain_file_page_id
            )

    def get_all_para_id_with_page_id(self, page_id: str) -> [str]:
        with DbSession.session_scope() as session:
            space_knowledge_domain_file_page_paras = (
                session.query(self.para_table)
                .filter(
                    self.para_table.c.space_knowledge_domain_file_page_id == page_id
                )
                .all()
            )
            list_of_para_ids = list()
            for (
                space_knowledge_domain_file_page_para
            ) in space_knowledge_domain_file_page_paras:
                list_of_para_ids.append(
                    space_knowledge_domain_file_page_para.space_knowledge_domain_file_page_para_id
                )
            return list_of_para_ids

    def delete_para_by_id(self, para_id: str):
        with DbSession.session_scope() as session:
            para = (
                session.query(self.para_table)
                .filter(
                    self.para_table.c.space_knowledge_domain_file_page_para_id
                    == para_id
                )
                .delete(synchronize_session=False)
            )
            # session.delete(para)
            session.commit()

    # Para Text
    def get_para_text_model(self):
        class SpaceKnowledgeDomainPageParaText(KnowledgeSpaceModels):
            __tablename__ = self.para_text_model_name

            para_id = Column(
                String,
                ForeignKey(
                    f"{self.para_model_name}.space_knowledge_domain_file_page_para_id"
                ),
                primary_key=True,
            )
            para_text = Column(String)

        return SpaceKnowledgeDomainPageParaText

    def get_para_text_model_name(self):
        return self.para_text_model_name

    def add_new_para_text(self, para_id: str, para_text: str):
        KnowledgeSpaceModels.metadata.reflect(bind=DbSession.get_engine())
        statement = (
            KnowledgeSpaceModels.metadata.tables[self.para_text_model_name]
            .insert()
            .values(para_id=para_id, para_text=para_text)
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()

    def get_para_text_all_id(self):
        with DbSession.session_scope() as session:
            para_text_ids = session.query(self.para_text_table.c.para_id).all()
            list_of_para_text_ids = list()
            for para_text_id in para_text_ids:
                list_of_para_text_ids.append(para_text_id)
            return list_of_para_text_ids

    def get_para_text_by_id(self, para_id: str):
        with DbSession.session_scope() as session:
            para_text = (
                session.query(self.para_text_table.c.para_text)
                .filter(self.para_text_table.c.para_id == para_id)
                .first()
            )
            return unicodedata.normalize("NFD", str(para_text))

    def delete_para_text_by_id(self, para_id: str):
        with DbSession.session_scope() as session:
            para_text = (
                session.query(self.para_text_table)
                .filter(self.para_text_table.c.para_id == para_id)
                .delete(synchronize_session=False)
            )
            session.commit()
        return

    # Domain QA Context
    def get_domain_qa_context_model(self):
        class SpaceKnowledgeDomainQAContext(KnowledgeSpaceModels):
            __tablename__ = self.domain_qa_context_model_name

            context_id = Column(String(255), primary_key=True)
            question = Column(String(255), nullable=False)
            answer = Column(String, nullable=False)
            answer_source_para_id = Column(
                String,
                ForeignKey(
                    f"{self.para_model_name}.space_knowledge_domain_file_page_para_id"
                ),
                nullable=False,
            )
            answered_at = Column(DateTime(), nullable=False)

        return SpaceKnowledgeDomainQAContext

    def get_domain_qa_context_model_name(self):
        return self.domain_qa_context_model_name

    def add_new_domain_qa_context(
        self, question: str, answer: str, answer_source_para_id: str
    ) -> str:
        KnowledgeSpaceModels.metadata.reflect(bind=DbSession.get_engine())
        context_id = gen_uuid()
        answered_at = format_timestamp_to_datetime(get_current_timestamp())
        statement = (
            KnowledgeSpaceModels.metadata.tables[self.domain_qa_context_model_name]
            .insert()
            .values(
                context_id=context_id,
                question=question,
                answer=answer,
                answer_source_para_id=answer_source_para_id,
                answered_at=answered_at,
            )
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return context_id

    def delete_domain_qa_context_with_para_id(self, para_id):
        KnowledgeSpaceModels.metadata.reflect(bind=DbSession.get_engine())
        with DbSession.session_scope() as session:
            domain_qa_context = (
                session.query(self.domain_qa_context_table)
                .filter(self.domain_qa_context_table.c.answer_source_para_id == para_id)
                .delete(synchronize_session=False)
            )
            session.commit()
