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

import resource
from google.protobuf.json_format import Parse

from drqa.retriever import TfidfDocRanker
from ethos.elint.entities.space_knowledge_domain_pb2 import SpaceKnowledgeDomain


def memory_usage():
    print(f"memory used: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1000000)}mb")


with open('/opt/ethos/apps/service/eapp-identity/tests/domain_dump.txt', 'r') as f:
    skd = Parse(f.read(), SpaceKnowledgeDomain())

with TfidfDocRanker(space_knowledge_domain=skd) as t:
    print(t.closest_docs('mathematics'))
    memory_usage()

memory_usage()
t1 = TfidfDocRanker(space_knowledge_domain=skd)
t1.closest_docs('mathematics')
memory_usage()
