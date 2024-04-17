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
import os
from datetime import datetime
from enum import Enum
from typing import Annotated, Optional

import requests
from autogen import ConversableAgent, ChatResult
from ethos.elint.entities.account_assistant_pb2 import AccountAssistantConnectedAccount, AccountAssistant
from ethos.elint.entities.account_pb2 import Account
from ethos.elint.entities.galaxy_pb2 import Galaxy
from ethos.elint.entities.generic_pb2 import ResponseMeta, PersistentSessionTokenDetails
from ethos.elint.entities.space_knowledge_domain_pb2 import SpaceKnowledgeDomain
from ethos.elint.entities.space_knowledge_pb2 import SpaceKnowledgeAction, SpaceKnowledge
from ethos.elint.entities.space_pb2 import Space
from ethos.elint.entities.universe_pb2 import Universe
from ethos.elint.services.product.action.space_knowledge_action_pb2 import DomainRankedAnswers
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2 import \
    AccountAssistantServicesAccessAuthDetails
from ethos.elint.services.product.identity.account_assistant.action_account_assistant_pb2 import \
    ActOnAccountMessageRequest
from ethos.elint.services.product.identity.account_assistant.action_account_assistant_pb2_grpc import \
    ActionAccountAssistantServiceServicer
from google.protobuf.any_pb2 import Any

from community.gramx.fifty.zero.ethos.identity.entities.account_assistant.access.consumers.access_account_assistant_consumer import \
    AccessAccountAssistantConsumer
from community.gramx.fifty.zero.ethos.identity.services_caller.account_assistant_message_service_caller import \
    send_message_to_account
from community.gramx.sixty.six.ethos.action.entities.space.knowledge.consumers.space_knowledge_action_consumer import \
    SpaceKnowledgeActionConsumer
from support.application.tracing import trace_rpc, AtlasTracer

EAPP_ACTION_GENERIC_LM_HOST = os.environ.get('EAPP_ACTION_GENERIC_LM_HOST', "generic_lm")
EAPP_ACTION_GENERIC_LM_PORT = os.environ.get('EAPP_ACTION_GENERIC_LM_PORT', "80")
EAPP_ACTION_GENERIC_LM_KEY = os.environ.get('EAPP_ACTION_GENERIC_LM_KEY', "sk-11111111111111111111111111111111")
EAPP_ACTION_GENERIC_LM_TYPE = os.environ.get('EAPP_ACTION_GENERIC_LM_TYPE', "")
EAPP_ACTION_GENERIC_LM_URI = f'{EAPP_ACTION_GENERIC_LM_HOST}:{EAPP_ACTION_GENERIC_LM_PORT}'
EAPP_ACTION_GENERIC_LM_MODEL = 'gpt-3.5-turbo'

from pydantic import BaseModel


class AccountModel(BaseModel):
    account_analytics_id: str
    account_id: str
    account_personal_email_id: str
    account_work_email_id: str
    account_country_code: str
    account_mobile_number: str
    account_first_name: str
    account_last_name: str
    account_galaxy_id: str
    account_birth_at: Optional[datetime]
    account_gender: str  # Assuming AccountGender is represented as a string
    created_at: Optional[datetime]
    account_billing_active: bool


class AccountAssistantModel(BaseModel):
    account_assistant_id: str
    account_assistant_name_code: int
    account_assistant_name: str
    account: AccountModel
    created_at: Optional[datetime]
    last_assisted_at: Optional[datetime]


class PersistentSessionTokenDetailsModel(BaseModel):
    session_token: str
    session_scope: str
    generated_at: datetime
    last_used_at: datetime
    valid_till: datetime


class AccountAssistantServicesAccessAuthDetailsModel(BaseModel):
    account_assistant: AccountAssistantModel
    account_assistant_services_access_session_token_details: PersistentSessionTokenDetailsModel
    requested_at: Optional[datetime]


class AccountAssistantConnectedAccountModel(BaseModel):
    account_connection_id: str
    account_id: str
    connected_at: datetime


class SpaceKnowledgeActionModel(str, Enum):
    ASK_QUESTION = "ASK_QUESTION"


class UniverseModel(BaseModel):
    universe_id: str
    big_bang_at: datetime
    universe_name: str
    universe_description: str


class GalaxyModel(BaseModel):
    galaxy_id: str
    galaxy_name: str
    universe: UniverseModel
    galaxy_created_at: datetime


class SpaceModel(BaseModel):
    galaxy: GalaxyModel  # Adjust the type according to the type of Galaxy
    space_id: str
    space_accessibility_type: str  # Adjust the type according to the type of SpaceAccessibilityType
    space_isolation_type: str  # Adjust the type according to the type of SpaceIsolationType
    space_entity_type: str  # Adjust the type according to the type of SpaceEntityType
    space_admin_id: str
    space_created_at: Optional[str]  # Adjust the type according to the type of space_created_at


class SpaceKnowledgeModel(BaseModel):
    space_knowledge_name: str
    space_knowledge_id: str
    space_knowledge_admin_account_id: str
    space: SpaceModel  # Adjust the type according to the type of space
    created_at: datetime  # Adjust the type according to the type of created_at


class SpaceKnowledgeDomainModel(BaseModel):
    space_knowledge_domain_id: str
    space_knowledge_domain_name: str
    space_knowledge_domain_description: str
    space_knowledge_domain_collar_enum: SpaceKnowledgeDomainCollarEnumModel
    space_knowledge_domain_isolated: bool
    space_knowledge: SpaceKnowledgeModel  # Adjust the type according to the type of space_knowledge
    created_at: Optional[str]  # Adjust the type according to the type of created_at
    last_updated_at: Optional[str]  # Adjust the type according to the type of last_updated_at


# Define Pydantic model for ActOnAccountMessageRequest
class ActOnAccountMessageRequestModel(BaseModel):
    access_auth_details: AccountAssistantServicesAccessAuthDetailsModel
    connected_account: AccountAssistantConnectedAccountModel
    space_knowledge_action: SpaceKnowledgeActionModel
    message: str
    act_on_particular_domain: bool
    space_knowledge_domain: SpaceKnowledgeDomainModel


class ActionAccountAssistantService(ActionAccountAssistantServiceServicer):
    def __init__(self):
        super(ActionAccountAssistantService, self).__init__()
        self.session_scope = self.__class__.__name__
        self.config_list = [
            {
                "model": f"{EAPP_ACTION_GENERIC_LM_MODEL}",
                "base_url": f"{EAPP_ACTION_GENERIC_LM_URI}/v1",
                "api_key": f"{EAPP_ACTION_GENERIC_LM_KEY}",
            }
        ]
        self.llm_config = {"config_list": self.config_list}

    @staticmethod
    def get_tool_response_content(chat_result: ChatResult):
        """
        This function extracts the content value from the first 'tool_responses' item in a ChatResult object.

        Args:
            chat_result: A dictionary representing a ChatResult object.

        Returns:
            The value for the key 'content' within the first 'tool_responses' item,
            or None if not found.
        """
        print("get_tool_response_content")
        # Check if chat_history exists and has elements
        if not chat_result.chat_history:
            print("get_tool_response_content, chat history none")
            return None

        for item in chat_result.chat_history:
            print(f"get_tool_response_content, item: {item}")
            # Look for the item with 'tool_responses' key
            if 'tool_responses' in item:
                # Get the first 'tool_responses' item
                tool_responses = item['tool_responses'][0]
                # Return the value for the key 'content'
                return tool_responses.get('content')

        # 'tool_responses' not found in chat_history
        return None

    @staticmethod
    def get_answer(input: Annotated[ActOnAccountMessageRequestModel, "Process an incoming request"]):
        request = ActOnAccountMessageRequest(
            access_auth_details=AccountAssistantServicesAccessAuthDetails(
                account_assistant=AccountAssistant(
                    account_assistant_id=input.access_auth_details.account_assistant.account_assistant_id,
                    created_at=input.access_auth_details.account_assistant.created_at,
                    account=Account(
                        account_id=input.access_auth_details.account_assistant.account.account_id,
                        created_at=input.access_auth_details.account_assistant.account.created_at,
                        account_gender=input.access_auth_details.account_assistant.account.account_gender,
                        account_birth_at=input.access_auth_details.account_assistant.account.account_birth_at,
                        account_first_name=input.access_auth_details.account_assistant.account.account_first_name,
                        account_last_name=input.access_auth_details.account_assistant.account.account_last_name,
                        account_galaxy_id=input.access_auth_details.account_assistant.account.account_galaxy_id,
                        account_country_code=input.access_auth_details.account_assistant.account.account_country_code,
                        account_billing_active=input.access_auth_details.account_assistant.account.account_billing_active,
                        account_mobile_number=input.access_auth_details.account_assistant.account.account_mobile_number,
                        account_analytics_id=input.access_auth_details.account_assistant.account.account_analytics_id,
                        account_work_email_id=input.access_auth_details.account_assistant.account.account_work_email_id,
                        account_personal_email_id=input.access_auth_details.account_assistant.account.account_personal_email_id
                    ),
                    account_assistant_name=input.access_auth_details.account_assistant.account_assistant_name,
                    account_assistant_name_code=input.access_auth_details.account_assistant.account_assistant_name_code,
                    last_assisted_at=input.access_auth_details.account_assistant.last_assisted_at,
                ),
                account_assistant_services_access_session_token_details=PersistentSessionTokenDetails(
                    session_token=input.access_auth_details.account_assistant_services_access_session_token_details.session_token,
                    session_scope=input.access_auth_details.account_assistant_services_access_session_token_details.session_scope,
                    valid_till=input.access_auth_details.account_assistant_services_access_session_token_details.valid_till,
                    generated_at=input.access_auth_details.account_assistant_services_access_session_token_details.generated_at,
                    last_used_at=input.access_auth_details.account_assistant_services_access_session_token_details.last_used_at,
                ),
                requested_at=input.access_auth_details.requested_at,
            ),
            message=input.message,
            connected_account=AccountAssistantConnectedAccount(
                account_connection_id=input.connected_account.account_connection_id,
                account_id=input.connected_account.account_id,
                connected_at=input.connected_account.connected_at,
            ),
            space_knowledge_action=input.space_knowledge_action,
            space_knowledge_domain=SpaceKnowledgeDomain(
                space_knowledge_domain_id=input.space_knowledge_domain.space_knowledge_domain_id,
                space_knowledge_domain_description=input.space_knowledge_domain.space_knowledge_domain_description,
                space_knowledge_domain_isolated=input.space_knowledge_domain.space_knowledge_domain_isolated,
                space_knowledge_domain_name=input.space_knowledge_domain.space_knowledge_domain_name,
                space_knowledge=SpaceKnowledge(
                    space_knowledge_name=input.space_knowledge_domain.space_knowledge.space_knowledge_name,
                    space_knowledge_id=input.space_knowledge_domain.space_knowledge.space_knowledge_id,
                    space_knowledge_admin_account_id=input.space_knowledge_domain.space_knowledge.space_knowledge_admin_account_id,
                    created_at=input.space_knowledge_domain.space_knowledge.created_at,
                    space=Space(
                        space_id=input.space_knowledge_domain.space_knowledge.space.space_id,
                        space_created_at=input.space_knowledge_domain.space_knowledge.space.space_created_at,
                        space_admin_id=input.space_knowledge_domain.space_knowledge.space.space_admin_id,
                        space_entity_type=input.space_knowledge_domain.space_knowledge.space.space_entity_type,
                        space_isolation_type=input.space_knowledge_domain.space_knowledge.space.space_isolation_type,
                        space_accessibility_type=input.space_knowledge_domain.space_knowledge.space.space_accessibility_type,
                        galaxy=Galaxy(
                            galaxy_id=input.space_knowledge_domain.space_knowledge.space.galaxy.galaxy_id,
                            galaxy_name=input.space_knowledge_domain.space_knowledge.space.galaxy.galaxy_name,
                            galaxy_created_at=input.space_knowledge_domain.space_knowledge.space.galaxy.galaxy_created_at,
                            universe=Universe(
                                universe_id=input.space_knowledge_domain.space_knowledge.space.galaxy.universe.universe_id,
                                universe_name=input.space_knowledge_domain.space_knowledge.space.galaxy.universe.universe_name,
                                universe_description=input.space_knowledge_domain.space_knowledge.space.galaxy.universe.universe_description,
                                big_bang_at=input.space_knowledge_domain.space_knowledge.space.galaxy.universe.big_bang_at
                            )
                        )
                    )
                )
            ),
            act_on_particular_domain=input.act_on_particular_domain,
        )
        logging.info(f"get_answer: input: {input}")
        if input.act_on_particular_domain:
            _, _, domains_ranked_answers = SpaceKnowledgeActionConsumer().ask_question(
                access_auth_details=request.access_auth_details,
                message=input.message, ask_particular_domain=True,
                space_knowledge_domain=request.space_knowledge_domain)
        else:
            _, _, domains_ranked_answers = SpaceKnowledgeActionConsumer().ask_question(
                access_auth_details=request.access_auth_details,
                message=input.message, ask_particular_domain=False,
                space_knowledge_domain=SpaceKnowledgeDomain())
        for domain_ranked_answer in domains_ranked_answers:
            print(
                f"{'-' * 20}{domain_ranked_answer.space_knowledge_domain.space_knowledge_domain_name}{'-' * 20}")
            for ranked_answer in domain_ranked_answer.ranked_answers:
                print(f"\t>{ranked_answer.para_rank}>>>{ranked_answer.answer}")
        message_sources = []
        msg, space_id, space_type_id, domain_id, context_id = ActionAccountAssistantService.resolve_best_answer(
            domains_ranked_answers)
        for domain_ranked_answer in domains_ranked_answers:
            message_source = Any()
            message_source.Pack(domain_ranked_answer)
            message_sources.append(message_source)
        logging.info(f"type(message_sources):{type(message_sources)}")
        return msg, space_id, space_type_id, domain_id, context_id, message_sources

    @staticmethod
    def get_answer_function(input: ActOnAccountMessageRequestModel):
        logging.info(f"get_answer_function: input: {input}")
        return ActionAccountAssistantService.get_answer(input)

    @trace_rpc()
    async def ActOnAccountMessage(self, request, context):
        logging.info("ActionAccountAssistantService:ActOnAccountMessage")
        access_consumer = AccessAccountAssistantConsumer
        validation_done, validation_message = access_consumer.validate_account_assistant_services(
            request.access_auth_details)
        AtlasTracer.set_span_attr("valid", validation_done)
        if validation_done is False:
            return ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        else:
            should_continue = True
            should_assist = False
            if request.space_knowledge_action == 0 and should_continue:
                assistant_agent = ConversableAgent(
                    name="Ethos_Assistant",
                    system_message="You are a helpful assistant. "
                                   "You can delegate the message to function based on the context for action and never answer directly based on your understanding."
                                   "Return 'TERMINATE' when the task is done.",
                    llm_config=self.llm_config,
                )
                user_proxy_agent = ConversableAgent("User", llm_config=False,
                                                    is_termination_msg=lambda msg: msg.get(
                                                        "content") is not None and "TERMINATE" in
                                                                                   msg[
                                                                                       "content"],
                                                    human_input_mode="NEVER", )
                # Assuming `request` is an instance of ActOnAccountMessageRequest
                assistant_agent.register_for_llm(name="ask_question", description="A question answering system")(
                    ActionAccountAssistantService.get_answer_function)
                user_proxy_agent.register_for_execution(name="ask_question")(
                    ActionAccountAssistantService.get_answer_function)
                chat_result = user_proxy_agent.initiate_chat(assistant_agent, message=request.message,
                                                             max_turns=2,
                                                             summary_method='reflection_with_llm')
                logging.info(f"chat_result: {chat_result}")
                msg, space_id, space_type_id, domain_id, context_id, message_sources = self.get_tool_response_content(
                    chat_result)
                response = send_message_to_account(
                    access_auth_details=request.access_auth_details,
                    connected_account=request.connected_account,
                    message=msg,
                    message_source_space_id=space_id,
                    message_source_space_type_id=space_type_id,
                    message_source_space_domain_id=domain_id,
                    message_source_space_domain_action=SpaceKnowledgeAction.ASK_QUESTION,
                    message_source_space_domain_action_context_id=context_id,
                    message_source=message_sources
                )
                return ResponseMeta(meta_done=validation_done, meta_message=validation_message)
            elif not should_continue:
                # step 1: find the message context (assistance context)
                # step 2: this context can be of zero-shot or 3-shot
                # step 3: this context pertains some actions to be done
                # step 4: this actions can be performed by the space assistant
                # step 4>: or domain assistants (who would need to act on message)
                # step 5: these assistants needs to respond back to space assistant
                # step 6: space assistant then responds with the apt assistance
                url = f"{EAPP_ACTION_GENERIC_LM_URI}/v1/chat/completions"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {EAPP_ACTION_GENERIC_LM_KEY}"
                }
                data = {
                    "model": f"{EAPP_ACTION_GENERIC_LM_TYPE}",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are Ethosai. Your. Personal. Conversational. Self learning. Distributed. "
                                       "Intelligent. Assistant."
                        },
                        {
                            "role": "user",
                            "content": f"{request.message}"
                        }
                    ],
                }

                response = requests.post(url, json=data, headers=headers)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    logging.info("API call successful!")
                    logging.info("Response:")
                    logging.info(response.json())
                    message = response.json()['choices'][0]['message']['content']
                else:
                    logging.info(f"API call failed with status code {response.status_code}")
                    logging.info("Response:")
                    logging.info(response.text)
                    message = "Apologies, I'm not available at the moment."

                response = send_message_to_account(
                    access_auth_details=request.access_auth_details,
                    connected_account=request.connected_account,
                    message=message,
                    message_source_space_id="space_id",
                    message_source_space_type_id="space_type_id",
                    message_source_space_domain_id="domain_id",
                    message_source_space_domain_action=SpaceKnowledgeAction.ASK_QUESTION,
                    message_source_space_domain_action_context_id="context_id",
                    message_source=[]
                )
                return ResponseMeta(meta_done=validation_done, meta_message=validation_message)
            else:
                return ResponseMeta(meta_done=False, meta_message="Invalid Action Requested.")

    @staticmethod
    def resolve_best_answer(domains_ranked_answers: [DomainRankedAnswers]) -> (str, str, str, str, str):
        """ returns params for the first best answer for the first found domain else empty tuple"""
        message = "I couldn't find any answers in any page in the space."
        message_source_space_knowledge_domain = None
        source_ranked_answer = ""
        for domain_ranked_answer in domains_ranked_answers:
            for ranked_answer in domain_ranked_answer.ranked_answers:
                message = ranked_answer.answer
                source_ranked_answer = ranked_answer
                message_source_space_knowledge_domain = domain_ranked_answer.space_knowledge_domain
                break
        if message_source_space_knowledge_domain is None:
            message_source_space_id = ""
            message_source_space_type_id = ""
            message_source_space_domain_id = ""
            message_source_space_domain_action_context_id = ""
        else:
            message_source_space_id = message_source_space_knowledge_domain.space_knowledge.space.space_id
            message_source_space_type_id = message_source_space_knowledge_domain.space_knowledge.space_knowledge_id
            message_source_space_domain_id = message_source_space_knowledge_domain.space_knowledge_domain_id
            message_source_space_domain_action_context_id = source_ranked_answer.context_id
        return (
            message, message_source_space_id, message_source_space_type_id, message_source_space_domain_id,
            message_source_space_domain_action_context_id)

# find the action
# send the request to particular action
# wait for the action response
# send account assistant message
