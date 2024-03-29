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

import os

from .. import DATA_DIR

DEFAULTS = {
    'db_path': os.path.join(DATA_DIR, 'wikipedia/docs.db'),
    'tfidf_path': os.path.join(
        DATA_DIR,
        'wikipedia/docs-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz'
    ),
    'elastic_url': 'localhost:9200'
}


def set_default(key, value):
    global DEFAULTS
    DEFAULTS[key] = value


def get_class(name):
    if name == 'ethosknowledge':
        return SpaceKnowledgeDomainFilePageDB
    if name == 'ethosknowledgepara':
        return SpaceKnowledgeDomainFilePageParaDB
    if name == 'tfidf':
        return TfidfDocRanker
    if name == 'sqlite':
        return DocDB
    if name == 'elasticsearch':
        return ElasticDocRanker
    raise RuntimeError('Invalid retriever class: %s' % name)


from .space_knowledge_domain_file_page_para_discover_service import SpaceKnowledgeDomainFilePageParaDB
from .space_knowledge_domain_file_page_discover_service import SpaceKnowledgeDomainFilePageDB
from .doc_db import DocDB
from .tfidf_doc_ranker import TfidfDocRanker
from .elastic_doc_ranker import ElasticDocRanker
