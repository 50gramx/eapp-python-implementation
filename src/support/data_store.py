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

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from ethos.elint.entities.galaxy_pb2 import Galaxy
from ethos.elint.entities.space_knowledge_domain_file_page_pb2 import SpaceKnowledgeDomainFilePage
from ethos.elint.entities.space_knowledge_domain_file_pb2 import SpaceKnowledgeDomainFile
from ethos.elint.entities.space_knowledge_domain_pb2 import SpaceKnowledgeDomain
from ethos.elint.entities.space_knowledge_pb2 import SpaceKnowledge
from ethos.elint.entities.space_pb2 import Space
from ethos.elint.entities.universe_pb2 import Universe


def _get_universe_id(universe: Universe):
    return f"{universe.universe_id}"


def _get_galaxy_key(galaxy: Galaxy):
    return f"{_get_universe_id(galaxy.universe)}/" \
           f"{galaxy.galaxy_id}"


def _get_space_key(space: Space):
    return f"{_get_galaxy_key(space.galaxy)}/" \
           f"{space.space_id}"


def _get_space_knowledge_key(space_knowledge: SpaceKnowledge):
    return f"{_get_space_key(space_knowledge.space)}/" \
           f"{space_knowledge.space_knowledge_id}"


def _get_space_knowledge_domain_key(space_knowledge_domain: SpaceKnowledgeDomain):
    return f"{_get_space_knowledge_key(space_knowledge_domain.space_knowledge)}/" \
           f"{space_knowledge_domain.space_knowledge_domain_id}"


def _get_space_knowledge_domain_tfidf_key(space_knowledge_domain: SpaceKnowledgeDomain):
    return f"{_get_space_knowledge_key(space_knowledge_domain.space_knowledge)}/" \
           f"{space_knowledge_domain.space_knowledge_domain_id}/tfidf"


def _get_space_knowledge_domain_file_key(space_knowledge_domain_file: SpaceKnowledgeDomainFile):
    return f"{_get_space_knowledge_domain_key(space_knowledge_domain_file.space_knowledge_domain)}/" \
           f"{space_knowledge_domain_file.space_knowledge_domain_file_id}"


def _get_space_knowledge_domain_file_page_key(space_knowledge_domain_file_page: SpaceKnowledgeDomainFilePage):
    return f"{_get_space_knowledge_domain_file_key(space_knowledge_domain_file_page.space_knowledge_domain_file)}/" \
           f"{space_knowledge_domain_file_page.space_knowledge_domain_file_page_id}"


class DataStore:

    # ------------------------------------
    # Initialisation of the class
    # ------------------------------------
    def __init__(self):
        self.access_id = os.environ['ELINT_STORE_ACCESS_KEY_ID']
        self.access_key = os.environ['ELINT_STORE_SECRET_ACCESS_KEY']
        self.bucket_name = os.environ['ELINT_STORE_BUCKET_NAME']
        self.region_name = os.environ['ELINT_STORE_REGION_NAME']
        self.ds_client_config = Config(
            region_name=self.region_name,
            retries={
                'max_attempts': 10,
                'mode': 'standard'
            }
        )
        self.endpoint = os.environ['ELINT_STORE_ENDPOINT']
        self.ds_client = boto3.client(
            's3',
            aws_access_key_id=self.access_id,
            aws_secret_access_key=self.access_key,
            endpoint_url=self.endpoint,
        )
        # Make bucket if not exist.
        try:
            self.ds_client.head_bucket(Bucket=self.bucket_name)
            print(f"Bucket '{self.bucket_name}' already exists")
        except ClientError as e:
            # If a client error is thrown, check if it was a 404 error (Bucket does not exist)
            error_code = e.response.get('Error', {}).get('Code')
            if error_code == '404':
                self.ds_client.create_bucket(Bucket=self.bucket_name)
            else:
                raise
        self.tmp_file_path = "/tmp"

    # ------------------------------------
    # Generic Client Functions
    # ------------------------------------
    def upload_file(self, source_file_path: str, target_file_key: str):
        self.ds_client.upload_file(
            source_file_path,
            self.bucket_name,
            target_file_key
        )
        return

    def download_file(self, source_file_key: str, target_file_path: str):
        self.ds_client.download_file(
            Bucket=self.bucket_name,
            Key=source_file_key,
            Filename=target_file_path
        )
        return

    def delete_file(self, source_file_key: str):
        self.ds_client.delete_object(
            Bucket=self.bucket_name,
            Key=source_file_key
        )
        return

    def put_object(self, object_key: str):
        self.ds_client.put_object(
            Bucket=self.bucket_name,
            Key=object_key
        )
        return

    def get_object_size(self, object_key: str):
        response = self.ds_client.head_object(
            Bucket=self.bucket_name,
            Key=object_key
        )
        return response['ContentLength']

    # ------------------------------------
    # Space Handlers
    # ------------------------------------
    def create_space(self, space: Space):
        self.put_object(object_key=f"{_get_space_key(space=space)}/")
        return

    # ------------------------------------
    # SpaceKnowledge Handlers
    # ------------------------------------
    def create_space_knowledge(self, space_knowledge: SpaceKnowledge):
        self.put_object(object_key=f"{_get_space_knowledge_key(space_knowledge=space_knowledge)}/")

    # ------------------------------------
    # SpaceKnowledgeDomain Handlers
    # ------------------------------------
    def create_space_knowledge_domain(self, space_knowledge_domain: SpaceKnowledgeDomain):
        self.put_object(object_key=f"{_get_space_knowledge_domain_key(space_knowledge_domain=space_knowledge_domain)}/")

    def get_tmp_domain_tfidf_path(self, domain: SpaceKnowledgeDomain):
        return f"{self.tmp_file_path}/{domain.space_knowledge_domain_id}"

    def upload_tmp_domain_tfidf(self, domain: SpaceKnowledgeDomain):
        self.upload_file(
            source_file_path=self.get_tmp_domain_tfidf_path(domain=domain),
            target_file_key=_get_space_knowledge_domain_tfidf_key(space_knowledge_domain=domain)
        )
        return

    def delete_tmp_domain_tfidf(self, domain: SpaceKnowledgeDomain):
        os.remove(self.get_tmp_domain_tfidf_path(domain=domain))

    # ------------------------------------
    # SpaceKnowledgeDomainFile Handlers
    # ------------------------------------
    def create_space_knowledge_domain_file(self, space_knowledge_domain_file: SpaceKnowledgeDomainFile):
        self.put_object(
            object_key=f"{_get_space_knowledge_domain_file_key(space_knowledge_domain_file=space_knowledge_domain_file)}")

    def get_tmp_filepath(self, file: SpaceKnowledgeDomainFile):
        return f"{self.tmp_file_path}/{file.space_knowledge_domain_file_id}"

    def upload_tmp_file(self, file: SpaceKnowledgeDomainFile):
        self.upload_file(
            source_file_path=self.get_tmp_filepath(file=file),
            target_file_key=_get_space_knowledge_domain_file_key(space_knowledge_domain_file=file)
        )
        return

    def delete_tmp_file(self, file: SpaceKnowledgeDomainFile):
        os.remove(self.get_tmp_filepath(file=file))

    def download_space_knowledge_domain_file(self, space_knowledge_domain_file: SpaceKnowledgeDomainFile):
        self.download_file(
            source_file_key=_get_space_knowledge_domain_file_key(
                space_knowledge_domain_file=space_knowledge_domain_file
            ),
            target_file_path=self.get_tmp_filepath(
                file=space_knowledge_domain_file
            )
        )
        return

    def delete_space_knowledge_domain_file(self, space_knowledge_domain_file: SpaceKnowledgeDomainFile):
        self.delete_file(
            source_file_key=_get_space_knowledge_domain_file_key(
                space_knowledge_domain_file=space_knowledge_domain_file)
        )
        return

    # ------------------------------------------------
    # SpaceKnowledgeDomainFilePage Handlers
    # ------------------------------------------------
    def get_tmp_page_filepath(self, page: SpaceKnowledgeDomainFilePage):
        return f"{self.tmp_file_path}/{page.space_knowledge_domain_file_page_id}.jpg"

    def upload_tmp_page(self, page: SpaceKnowledgeDomainFilePage):
        self.upload_file(
            source_file_path=self.get_tmp_page_filepath(page=page),
            target_file_key=_get_space_knowledge_domain_file_page_key(space_knowledge_domain_file_page=page)
        )
        return

    def delete_tmp_page(self, page: SpaceKnowledgeDomainFilePage):
        if os.path.exists(self.get_tmp_page_filepath(page=page)):
            os.remove(self.get_tmp_page_filepath(page=page))
        return

    def download_space_knowledge_domain_file_page(self, space_knowledge_domain_file_page: SpaceKnowledgeDomainFilePage):
        self.download_file(
            source_file_key=_get_space_knowledge_domain_file_page_key(
                space_knowledge_domain_file_page=space_knowledge_domain_file_page
            ),
            target_file_path=self.get_tmp_page_filepath(
                page=space_knowledge_domain_file_page
            )
        )
        return

    def delete_space_knowledge_domain_file_page(self, space_knowledge_domain_file_page: SpaceKnowledgeDomainFilePage):
        self.delete_file(
            source_file_key=_get_space_knowledge_domain_file_page_key(
                space_knowledge_domain_file_page=space_knowledge_domain_file_page)
        )
        return
