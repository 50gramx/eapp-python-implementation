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

# #!/usr/bin/env python3
#
#   ETHOS CONFIDENTIAL
#   __________________
#
#    [2020] - [Present] Ethos Assistance Incorporated.
#    All Rights Reserved.
#
#

"""Rank documents with TF-IDF scores"""

import logging
import os
from functools import partial
from multiprocessing.pool import ThreadPool

import numpy as np
import scipy.sparse as sp

from ethos.elint.entities.space_knowledge_domain_pb2 import SpaceKnowledgeDomain
from support.data_store import DataStore
from . import utils
from .. import tokenizers

logger = logging.getLogger(__name__)


def validate_domain_tfidf_path(domain: SpaceKnowledgeDomain) -> str:
    # download domain tfidf from data store if not available on disk
    tfidf_path = DataStore().get_tmp_domain_tfidf_path(domain=domain)
    if not os.path.exists(tfidf_path):
        if not os.path.isfile(tfidf_path):
            DataStore().download_space_knowledge_domain_tfidf(domain=domain)
    elif not match_domain_tfidf_on_disk(domain):
        DataStore().download_space_knowledge_domain_tfidf(domain=domain)
    return tfidf_path


def match_domain_tfidf_on_disk(domain):
    # domain_size_on_disk = os.stat(DataStore().get_tmp_domain_tfidf_path(domain=domain)).st_size
    # domain_size_on_store = DataStore().get_object_size(
    #     object_key=_get_space_knowledge_domain_tfidf_key(space_knowledge_domain=domain))
    # return domain_size_on_disk == domain_size_on_store
    return True


class TfidfDocRanker(object):
    """Loads a pre-weighted inverted index of token/document terms.
    Scores new queries by taking sparse dot products.
    """

    # storage for the instance reference
    __domain_list = []
    __domain_instance = None

    def __init__(self, space_knowledge_domain: SpaceKnowledgeDomain, strict=True):
        domain_id = space_knowledge_domain.space_knowledge_domain_id
        if domain_id not in TfidfDocRanker.__domain_list:
            TfidfDocRanker.__domain_instance = TfidfDocRanker.__impl(
                space_knowledge_domain=space_knowledge_domain, strict=strict)
            TfidfDocRanker.__domain_list.append(domain_id)
            logging.critical(f"New TfidfDocRanker instance with id {domain_id}")
        self.__dict__['_TfidfDocRanker__domain_instance'] = TfidfDocRanker.__domain_instance

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__domain_instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__domain_instance, attr, value)

    class __impl:
        """ Implementation of the singleton interface """

        def __init__(self, space_knowledge_domain: SpaceKnowledgeDomain, strict=True):
            """
            Args:
                tfidf_path: path to saved model file
                strict: fail on empty queries or continue (and return empty result)
            """
            # Load from disk
            tfidf_path = validate_domain_tfidf_path(domain=space_knowledge_domain)
            logger.info('Loading %s' % tfidf_path)
            matrix, metadata = utils.load_sparse_csr(tfidf_path)
            self.doc_mat = matrix
            self.ngrams = metadata['ngram']
            self.hash_size = metadata['hash_size']
            self.tokenizer = tokenizers.get_class(metadata['tokenizer'])()
            self.doc_freqs = metadata['doc_freqs'].squeeze()
            self.doc_dict = metadata['doc_dict']
            self.num_docs = len(self.doc_dict[0])
            self.strict = strict

        def get_doc_index(self, doc_id):
            """Convert doc_id --> doc_index"""
            return self.doc_dict[0][doc_id]

        def get_doc_id(self, doc_index):
            """Convert doc_index --> doc_id"""
            return self.doc_dict[1][doc_index]

        def closest_docs(self, query, k=1):
            """Closest docs by dot product between query and documents
            in tfidf weighted word vector space.
            """
            spvec = self.text2spvec(query)
            res = spvec * self.doc_mat

            if len(res.data) <= k:
                o_sort = np.argsort(-res.data)
            else:
                o = np.argpartition(-res.data, k)[0:k]
                o_sort = o[np.argsort(-res.data[o])]

            doc_scores = res.data[o_sort]
            doc_ids = [self.get_doc_id(i) for i in res.indices[o_sort]]
            return doc_ids, doc_scores

        def batch_closest_docs(self, queries, k=1, num_workers=None):
            """Process a batch of closest_docs requests multithreaded.
            Note: we can use plain threads here as scipy is outside of the GIL.
            """
            with ThreadPool(num_workers) as threads:
                closest_docs = partial(self.closest_docs, k=k)
                results = threads.map(closest_docs, queries)
            return results

        def parse(self, query):
            """Parse the query into tokens (either ngrams or tokens)."""
            tokens = self.tokenizer.tokenize(query)
            return tokens.ngrams(n=self.ngrams, uncased=True,
                                 filter_fn=utils.filter_ngram)

        def text2spvec(self, query):
            """Create a sparse tfidf-weighted word vector from query.

            tfidf = log(tf + 1) * log((N - Nt + 0.5) / (Nt + 0.5))
            """
            # Get hashed ngrams
            words = self.parse(utils.normalize(query))
            wids = [utils.hash(w, self.hash_size) for w in words]

            if len(wids) == 0:
                if self.strict:
                    raise RuntimeError('No valid word in: %s' % query)
                else:
                    logger.warning('No valid word in: %s' % query)
                    return sp.csr_matrix((1, self.hash_size))

            # Count TF
            wids_unique, wids_counts = np.unique(wids, return_counts=True)
            tfs = np.log1p(wids_counts)

            # Count IDF
            Ns = self.doc_freqs[wids_unique]
            idfs = np.log((self.num_docs - Ns + 0.5) / (Ns + 0.5))
            idfs[idfs < 0] = 0

            # TF-IDF
            data = np.multiply(tfs, idfs)

            # One row, sparse csr matrix
            indptr = np.array([0, len(wids_unique)])
            spvec = sp.csr_matrix(
                (data, wids_unique, indptr), shape=(1, self.hash_size)
            )

            return spvec
