#   /*************************************************************************
#   *
#   * AMIT KUMAR KHETAN CONFIDENTIAL
#   * __________________
#   *
#   *  [2017] - [2024] Amit Kumar Khetan
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


from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.cognitive.assist.knowledge.reader_knowledge_pb2 import ReadPageQuestionResponse, PageAnswer, \
    ReadParaQuestionResponse, ParaAnswer
from ethos.elint.services.cognitive.assist.knowledge.reader_knowledge_pb2_grpc import ReaderKnowledgeServiceServicer

from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.access.consumers.access_space_knowledge_domain_consumer import \
    AccessSpaceKnowledgeDomainConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file_page.discover.consumers.discover_space_knowledge_domain_file_page_consumer import \
    DiscoverSpaceKnowledgeDomainFilePageConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file_page_para.discover.consumers.discover_space_knowledge_domain_file_page_para_consumer import \
    DiscoverSpaceKnowledgeDomainFilePageParaConsumer
from community.gramx.sixty.six.ethos.reader.entities.knowledge.reader.question_answer import QuestionAnswer


class ReaderKnowledgeService(ReaderKnowledgeServiceServicer):
    def __init__(self):
        super(ReaderKnowledgeService, self).__init__()
        self.session_scope = self.__class__.__name__

    def ReadPageQuestion(self, request, context):
        print("ReaderKnowledgeService:ReadPageQuestion")
        domain_consumer = AccessSpaceKnowledgeDomainConsumer()
        validation_done, validation_message = domain_consumer.validate_space_knowledge_domain_services(
            request.access_auth_details)
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return ReadPageQuestionResponse(response_meta=meta)
        else:
            page_consumer = DiscoverSpaceKnowledgeDomainFilePageConsumer()
            _, _, page_text = page_consumer.get_page_text_by_id(access_auth_details=request.access_auth_details,
                                                                page_id=request.page.space_knowledge_domain_file_page_id)
            qa = QuestionAnswer()
            question_context = page_text.replace('\t', '').replace('\n', '').replace('\ t', '').replace('\ n', '')
            # for i in range(0, len(question_context), 300):
            #     qc = question_context[i:i + 300]
            #     print(f"Answer: {qa.get_page_answer(question=request.question, page_text=qc)}")
            print(f"para: {question_context}")
            answer = qa.get_page_answer(question=request.question,
                                        page_text=question_context)

            page_answer = PageAnswer(answer=answer, page_text=page_text)
            return ReadPageQuestionResponse(page_answer=page_answer, response_meta=meta)

    def ReadParaQuestion(self, request, context):
        print("ReaderKnowledgeService:ReadParaQuestion")
        domain_consumer = AccessSpaceKnowledgeDomainConsumer()
        validation_done, validation_message = domain_consumer.validate_space_knowledge_domain_services(
            request.access_auth_details)
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return ReadParaQuestionResponse(response_meta=meta)
        else:
            para_consumer = DiscoverSpaceKnowledgeDomainFilePageParaConsumer()
            _, _, para_text = para_consumer.get_para_text_by_id(access_auth_details=request.access_auth_details,
                                                                para_id=request.para.space_knowledge_domain_file_page_para_id)
            qa = QuestionAnswer()
            question_context = para_text.replace('\t', '').replace('\n', '').replace('\ t', '').replace('\ n', '')
            # TODO: Make sure, para contents is not more than 500 characters
            # print('-'*30)
            # print(f"{question_context}")
            # print('-' * 30)
            answer = qa.get_para_answer(question=request.question,
                                        para_text=question_context)
            para_answer = ParaAnswer(answer=answer, para_text=para_text)
            return ReadParaQuestionResponse(para_answer=para_answer, response_meta=meta)
