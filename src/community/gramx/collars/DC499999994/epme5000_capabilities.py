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

from ethos.elint.collars.DC499999994_caps_pb2 import RepeatedDC499999994
from ethos.elint.collars.DC499999994_caps_pb2_grpc import (
    DC499999994EPME5000CapabilitiesServicer,
)
from ethos.elint.collars.DC499999994_pb2 import SkincareProduct
from ethos.elint.entities.generic_pb2 import ResponseMeta

from src.community.gramx.collars.DC499999994.model import DC499999994Model
from src.community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.create.consumers.create_space_knowledge_domain_consumer import (
    CreateSpaceKnowledgeDomainConsumer,
)
from src.community.gramx.fifty.zero.ethos.product_spaces.entities.space_product_domain.access.consumers.access_space_product_domain_consumer import (
    AccessSpaceProductDomainConsumer,
)
from support.application.tracing import trace_rpc


class DC499999994EPME5000Capabilities(DC499999994EPME5000CapabilitiesServicer):
    def __init__(self):
        super(DC499999994EPME5000Capabilities, self).__init__()
        self.session_scope = self.__class__.__name__
        self.ccode = "DC499999994"

    @trace_rpc()
    def Create(self, request, context):
        logging.info(f"{self.session_scope}:Create")
        logging.info(f"{self.session_scope}:Create: request: {request}")
        done, msg = (
            AccessSpaceProductDomainConsumer.validate_space_product_domain_services(
                request.spd_auth
            )
        )
        meta = ResponseMeta(meta_done=done, meta_message=msg)
        if done is False:
            return meta
        else:
            spd_auth = request.spd_auth
            spd = spd_auth.space_product_domain
            skincare_product = request.skincare_product

            # TODO: request for creating space knowledge domain for product image files
            # product_images_domain
            kd_res = CreateSpaceKnowledgeDomainConsumer.create_space_knowledge_domain(
                kauth=request.sk_auth,
                name=f"{skincare_product.name} Images",
                desc="Images of the skin care products",
                cnum=0,
                isol=spd.is_isolated,
            )
            kd_auth = kd_res.space_knowledge_domain_services_access_auth_details
            kd = kd_auth.space_knowledge_domain

            # objective: add the skincare_product to the database
            # load the db

            cmodel = DC499999994Model(
                space_product_domain_id=spd.id,
                space_product_domain_collar_code=self.ccode,
            )
            # insert skincare_product
            did = cmodel.add_skincare_product_from_proto(
                skincare_product_proto=skincare_product
            )
            # insert collar
            cid = cmodel.add_collar(
                skincare_product_id=did,
                name=skincare_product.name,
                images_sk_id=kd.space_knowledge.space_knowledge_id,
                images_skd_id=kd.space_knowledge_domain_id,
            )

            # add this kd to someplace so all products in the collar
            #  use this kd for storing and managing photos

            logging.info(f"Skincare Product created. cid='{cid}'")

            return meta

    @trace_rpc()
    def List(self, request, context):
        logging.info(f"{self.session_scope}:List")
        done, msg = (
            AccessSpaceProductDomainConsumer.validate_space_product_domain_services(
                request
            )
        )
        meta = ResponseMeta(meta_done=done, meta_message=msg)
        if done is False:
            return meta
        else:
            # load the db
            cmodel = DC499999994Model(
                space_product_domain_id=request.space_product_domain.id,
                space_product_domain_collar_code=self.ccode,
            )
            # get list of collars
            cs = cmodel.get_collar_all()
            return RepeatedDC499999994(collars=cs, meta=meta)

    @trace_rpc()
    def Get(self, request, context):
        logging.info(f"{self.session_scope}:Get")
        done, msg = (
            AccessSpaceProductDomainConsumer.validate_space_product_domain_services(
                request.auth
            )
        )
        meta = ResponseMeta(meta_done=done, meta_message=msg)
        if done is False:
            return SkincareProduct()
        else:
            # load the db
            cmodel = DC499999994Model(
                space_product_domain_id=request.auth.space_product_domain.id,
                space_product_domain_collar_code=self.ccode,
            )
            # get list of collars
            c = cmodel.get_collar(id=request.collar_id, sk_auth=request.sk_auth)

            return c
