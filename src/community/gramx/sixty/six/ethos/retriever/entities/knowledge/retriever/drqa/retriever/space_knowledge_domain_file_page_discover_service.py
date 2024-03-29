#!/usr/bin/env python3
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
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
"""Documents, in a sqlite database."""

import os

import psycopg2

from . import DEFAULTS
from . import utils

db_user = os.environ['EA_KB_DB_USER']
db_pass = os.environ['EA_KB_DB_PASS']
db_host = os.environ['EA_KB_DB_HOST']
db_port = os.environ['EA_KB_DB_PORT']
db_name = os.environ['EA_KB_DB_NAME']


class SpaceKnowledgeDomainFilePageDB(object):
    """Sqlite backed document storage.

    Implements get_doc_text(doc_id).
    """

    def __init__(self, space_knowledge_domain_id: str, db_path=None):
        self.path = db_path or DEFAULTS['db_path']
        self.connection = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_pass)
        self.page_table_name = f"skdfpt_{space_knowledge_domain_id}"

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def path(self):
        """Return the path to the file that backs this database."""
        return self.path

    def close(self):
        """Close the connection to the database."""
        self.connection.close()

    def get_doc_ids(self):
        """Fetch all ids of docs stored in the db."""
        cursor = self.connection.cursor()
        cursor.execute(f'SELECT page_id FROM "{self.page_table_name}"')
        results = [r[0] for r in cursor.fetchall()]
        cursor.close()
        return results

    def get_doc_text(self, page_id):
        """Fetch the raw text of the doc for 'doc_id'."""
        cursor = self.connection.cursor()
        cursor.execute(
            f'SELECT page_text FROM "{self.page_table_name}" WHERE page_id = %s',
            (page_id,)
        )
        result = cursor.fetchone()
        cursor.close()
        return result if result is None else result[0]
