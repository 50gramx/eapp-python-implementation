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
"""A script to build the tf-idf document matrices for retrieval."""

import logging
import math
from collections import Counter
from functools import partial
from multiprocessing import Pool as ProcessPool
from types import SimpleNamespace

import numpy as np
import scipy.sparse as sp
from multiprocessing.util import Finalize

from community.gramx.sixty.six.ethos.retriever.entities.knowledge.retriever.drqa import tokenizers, retriever

logger = logging.getLogger()
logger.setLevel(logging.INFO)
fmt = logging.Formatter('%(asctime)s: [ %(message)s ]', '%m/%d/%Y %I:%M:%S %p')
console = logging.StreamHandler()
console.setFormatter(fmt)
logger.addHandler(console)

# ------------------------------------------------------------------------------
# Multiprocessing functions
# ------------------------------------------------------------------------------

DOC2IDX = None
PROCESS_TOK = None
PROCESS_DB = None


def init(tokenizer_class, db_class, db_opts):
    global PROCESS_TOK, PROCESS_DB
    PROCESS_TOK = tokenizer_class()
    Finalize(PROCESS_TOK, PROCESS_TOK.shutdown, exitpriority=100)
    PROCESS_DB = db_class(**db_opts)
    Finalize(PROCESS_DB, PROCESS_DB.close, exitpriority=100)


def fetch_text(doc_id):
    global PROCESS_DB
    return PROCESS_DB.get_doc_text(doc_id)


def tokenize(text):
    global PROCESS_TOK
    return PROCESS_TOK.tokenize(text)


# ------------------------------------------------------------------------------
# Build article --> word count sparse matrix.
# ------------------------------------------------------------------------------


def count(ngram, hash_size, DOC2IDX, doc_id):
    """Fetch the text of a document and compute hashed ngrams counts."""
    # global DOC2IDX
    row, col, data = [], [], []
    # Tokenize
    tokens = tokenize(retriever.utils.normalize(fetch_text(doc_id)))

    # Get ngrams from tokens, with stopword/punctuation filtering.
    ngrams = tokens.ngrams(
        n=ngram, uncased=True, filter_fn=retriever.utils.filter_ngram
    )

    # Hash ngrams and count occurences
    counts = Counter([retriever.utils.hash(gram, hash_size) for gram in ngrams])

    # Return in sparse matrix data format.
    row.extend(counts.keys())
    print(f"DOC2IDX: {DOC2IDX}")
    col.extend([DOC2IDX[doc_id]] * len(counts))
    data.extend(counts.values())
    return row, col, data


def get_count_matrix(args, db, db_opts):
    """Form a sparse word to document count matrix (inverted index).

    M[i, j] = # times word i appears in document j.
    """
    # Map doc_ids to indexes
    global DOC2IDX
    db_class = retriever.get_class(db)
    with db_class(**db_opts) as doc_db:
        doc_ids = doc_db.get_doc_ids()
    print(f"doc_ids: {doc_ids}")
    DOC2IDX = {doc_id: i for i, doc_id in enumerate(doc_ids)}
    print(f"DOC2IDX: {DOC2IDX}")

    # Setup worker pool
    tok_class = tokenizers.get_class(args.tokenizer)
    workers = ProcessPool(
        args.num_workers,
        initializer=init,
        initargs=(tok_class, db_class, db_opts)
    )

    # Compute the count matrix in steps (to keep in memory)
    logger.info('Mapping...')
    row, col, data = [], [], []
    step = max(int(len(doc_ids) / 10), 1)
    batches = [doc_ids[i:i + step] for i in range(0, len(doc_ids), step)]
    _count = partial(count, args.ngram, args.hash_size, DOC2IDX)
    for i, batch in enumerate(batches):
        logger.info('-' * 25 + 'Batch %d/%d' % (i + 1, len(batches)) + '-' * 25)
        for b_row, b_col, b_data in workers.imap_unordered(_count, batch):
            row.extend(b_row)
            col.extend(b_col)
            data.extend(b_data)
    workers.close()
    workers.join()

    logger.info('Creating sparse matrix...')
    count_matrix = sp.csr_matrix(
        (data, (row, col)), shape=(args.hash_size, len(doc_ids))
    )
    count_matrix.sum_duplicates()
    return count_matrix, (DOC2IDX, doc_ids)


# ------------------------------------------------------------------------------
# Transform count matrix to different forms.
# ------------------------------------------------------------------------------


def get_tfidf_matrix(cnts):
    """Convert the word count matrix into tfidf one.

    tfidf = log(tf + 1) * log((N - Nt + 0.5) / (Nt + 0.5))
    * tf = term frequency in document
    * N = number of documents
    * Nt = number of occurences of term in all documents
    """
    Ns = get_doc_freqs(cnts)
    idfs = np.log((cnts.shape[1] - Ns + 0.5) / (Ns + 0.5))
    idfs[idfs < 0] = 0
    idfs = sp.diags(idfs, 0)
    tfs = cnts.log1p()
    tfidfs = idfs.dot(tfs)
    return tfidfs


def get_doc_freqs(cnts):
    """Return word --> # of docs it appears in."""
    binary = (cnts > 0).astype(int)
    freqs = np.array(binary.sum(1)).squeeze()
    return freqs


# ------------------------------------------------------------------------------
# Main.
# ------------------------------------------------------------------------------


def build_domain_tfidf(
        space_knowledge_domain_id: str, out_dir: str, ngram: int = 2,
        hash_size: int = int(math.pow(2, 24)), tokenizer: str = 'simple',
        num_workers: int = None
) -> str:
    args = SimpleNamespace(
        space_knowledge_domain_id=space_knowledge_domain_id,
        out_dir=out_dir,
        ngram=ngram,
        hash_size=hash_size,
        tokenizer=tokenizer,
        num_workers=num_workers
    )
    logging.info('Counting words...')
    count_matrix, doc_dict = get_count_matrix(
        args, 'ethosknowledge', {'space_knowledge_domain_id': args.space_knowledge_domain_id}
    )

    logger.info('Making tfidf vectors...')
    tfidf = get_tfidf_matrix(count_matrix)

    logger.info('Getting word-doc frequencies...')
    freqs = get_doc_freqs(count_matrix)

    # basename = os.path.splitext(os.path.basename(args.db_path))[0]
    # basename = args.space_knowledge_domain_id
    # basename += ('-tfidf-ngram=%d-hash=%d-tokenizer=%s' %
    #              (args.ngram, args.hash_size, args.tokenizer))
    # filename = os.path.join(args.out_dir, basename)
    filename = args.out_dir

    logger.info('Saving to %s' % filename)
    metadata = {
        'doc_freqs': freqs,
        'tokenizer': args.tokenizer,
        'hash_size': args.hash_size,
        'ngram': args.ngram,
        'doc_dict': doc_dict
    }
    retriever.utils.save_sparse_csr(filename, tfidf, metadata)
    return filename


def build_domain_para_tfidf(
        space_knowledge_domain_id: str, out_dir: str, ngram: int = 2,
        hash_size: int = int(math.pow(2, 24)), tokenizer: str = 'simple',
        num_workers: int = None
) -> str:
    args = SimpleNamespace(
        space_knowledge_domain_id=space_knowledge_domain_id,
        out_dir=out_dir,
        ngram=ngram,
        hash_size=hash_size,
        tokenizer=tokenizer,
        num_workers=num_workers
    )
    logging.info('Counting words...')
    count_matrix, doc_dict = get_count_matrix(
        args, 'ethosknowledgepara', {'space_knowledge_domain_id': args.space_knowledge_domain_id}
    )

    logger.info('Making tfidf vectors...')
    tfidf = get_tfidf_matrix(count_matrix)

    logger.info('Getting word-doc frequencies...')
    freqs = get_doc_freqs(count_matrix)

    # basename = os.path.splitext(os.path.basename(args.db_path))[0]
    # basename = args.space_knowledge_domain_id
    # basename += ('-tfidf-ngram=%d-hash=%d-tokenizer=%s' %
    #              (args.ngram, args.hash_size, args.tokenizer))
    # filename = os.path.join(args.out_dir, basename)
    filename = args.out_dir

    logger.info('Saving to %s' % filename)
    metadata = {
        'doc_freqs': freqs,
        'tokenizer': args.tokenizer,
        'hash_size': args.hash_size,
        'ngram': args.ngram,
        'doc_dict': doc_dict
    }
    retriever.utils.save_sparse_csr(filename, tfidf, metadata)
    return filename

#
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument('space_knowledge_domain_id', type=str, default=None,
#                         help='Space Knowledge Domain ID for Access')
#     # parser.add_argument('db_path', type=str, default=None,
#     #                     help='Path to sqlite db holding document texts')
#     parser.add_argument('out_dir', type=str, default=None,
#                         help='Directory for saving output files')
#     parser.add_argument('--ngram', type=int, default=2,
#                         help=('Use up to N-size n-grams '
#                               '(e.g. 2 = unigrams + bigrams)'))
#     parser.add_argument('--hash-size', type=int, default=int(math.pow(2, 24)),
#                         help='Number of buckets to use for hashing ngrams')
#     parser.add_argument('--tokenizer', type=str, default='simple',
#                         help=("String option specifying tokenizer type to use "
#                               "(e.g. 'corenlp')"))
#     parser.add_argument('--num-workers', type=int, default=None,
#                         help='Number of CPU processes (for tokenizing, etc)')
#     args = parser.parse_args()
#     print(f"type: {type(args)}, args: {args}")

# logging.info('Counting words...')
# count_matrix, doc_dict = get_count_matrix(
#     args, 'ethosknowledge', {'space_knowledge_domain_id': args.space_knowledge_domain_id}
# )
#
# logger.info('Making tfidf vectors...')
# tfidf = get_tfidf_matrix(count_matrix)
#
# logger.info('Getting word-doc frequencies...')
# freqs = get_doc_freqs(count_matrix)
#
# # basename = os.path.splitext(os.path.basename(args.db_path))[0]
# basename = args.space_knowledge_domain_id
# basename += ('-tfidf-ngram=%d-hash=%d-tokenizer=%s' %
#              (args.ngram, args.hash_size, args.tokenizer))
# filename = os.path.join(args.out_dir, basename)
#
# logger.info('Saving to %s.npz' % filename)
# metadata = {
#     'doc_freqs': freqs,
#     'tokenizer': args.tokenizer,
#     'hash_size': args.hash_size,
#     'ngram': args.ngram,
#     'doc_dict': doc_dict
# }
# retriever.utils.save_sparse_csr(filename, tfidf, metadata)
