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

import proto
import requests
from autogen import ChatResult, ConversableAgent
from autogen.agentchat.contrib.multimodal_conversable_agent import (
    MultimodalConversableAgent,  # for GPT-4V
)
from ethos.elint.entities.account_assistant_pb2 import (
    AccountAssistant,
    AccountAssistantConnectedAccount,
)
from ethos.elint.entities.account_pb2 import Account
from ethos.elint.entities.galaxy_pb2 import Galaxy
from ethos.elint.entities.generic_pb2 import PersistentSessionTokenDetails, ResponseMeta
from ethos.elint.entities.space_knowledge_domain_pb2 import SpaceKnowledgeDomain
from ethos.elint.entities.space_knowledge_pb2 import (
    SpaceKnowledge,
    SpaceKnowledgeAction,
)
from ethos.elint.entities.space_pb2 import Space
from ethos.elint.entities.space_product_domain_pb2 import SpaceProductDomain
from ethos.elint.entities.space_product_pb2 import SpaceProduct
from ethos.elint.entities.space_service_pb2 import SpaceService
from ethos.elint.entities.universe_pb2 import Universe
from ethos.elint.services.product.action.space_knowledge_action_pb2 import (
    DomainRankedAnswers,
)
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2 import (
    AccountAssistantServicesAccessAuthDetails,
)
from ethos.elint.services.product.identity.account_assistant.action_account_assistant_pb2 import (
    ActOnAccountMessageRequest,
)
from ethos.elint.services.product.identity.account_assistant.action_account_assistant_pb2_grpc import (
    ActionAccountAssistantServiceServicer,
)
from ethos.elint.services.product.identity.space.access_space_pb2 import (
    SpaceServicesAccessAuthDetails,
)
from ethos.elint.services.product.knowledge.space_knowledge.access_space_knowledge_pb2 import (
    SpaceKnowledgeServicesAccessAuthDetails,
)
from ethos.elint.services.product.product.space_product.access_space_product_pb2 import (
    SpaceProductServicesAccessAuthDetails,
)
from ethos.elint.services.product.service.space_service.access_space_service_pb2 import (
    SpaceServiceServicesAccessAuthDetails,
)
from google.protobuf.any_pb2 import Any
from google.protobuf.json_format import MessageToDict

from community.gramx.fifty.zero.ethos.identity.entities.account_assistant.access.consumers.access_account_assistant_consumer import (
    AccessAccountAssistantConsumer,
)
from community.gramx.fifty.zero.ethos.identity.services_caller.account_assistant_message_service_caller import (
    send_message_to_account,
)
from community.gramx.sixty.six.ethos.action.entities.space.knowledge.consumers.space_knowledge_action_consumer import (
    SpaceKnowledgeActionConsumer,
)
from src.community.gramx.collars.DC499999994.epme5000_consumer import (
    DC499999994EPME5000Consumer,
)
from src.community.gramx.fifty.zero.ethos.identity.entities.space.access.consumers.access_space_consumer import (
    AccessSpaceConsumer,
)
from src.community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge.access.consumers.access_space_knowledge_consumer import (
    AccessSpaceKnowledgeConsumer,
)
from src.community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge.discover.consumers.discover_space_knowledge_consumer import (
    DiscoverSpaceKnowledgeConsumer,
)
from src.community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.access.consumers.access_space_knowledge_domain_consumer import (
    AccessSpaceKnowledgeDomainConsumer,
)
from src.community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.discover.consumers.discover_space_knowledge_domain_consumer import (
    DiscoverSpaceKnowledgeDomainConsumer,
)
from src.community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file.discover.consumers.discover_space_knowledge_domain_file_consumer import (
    DiscoverSpaceKnowledgeDomainFileConsumer,
)
from src.community.gramx.fifty.zero.ethos.product_spaces.entities.space_product.access.consumers.access_space_product_consumer import (
    AccessSpaceProductConsumer,
)
from src.community.gramx.fifty.zero.ethos.product_spaces.entities.space_product.discover.consumers.discover_space_product_consumer import (
    DiscoverSpaceProductConsumer,
)
from src.community.gramx.fifty.zero.ethos.product_spaces.entities.space_product_domain.access.consumers.access_space_product_domain_consumer import (
    AccessSpaceProductDomainConsumer,
)
from src.community.gramx.fifty.zero.ethos.service_spaces.entities.space_service.access.consumers.access_space_service_consumer import (
    AccessSpaceServiceConsumer,
)
from src.community.gramx.fifty.zero.ethos.service_spaces.entities.space_service.discover.consumers.discover_space_service_consumer import (
    DiscoverSpaceServiceConsumer,
)
from support.application.tracing import AtlasTracer, trace_rpc

EAPP_ACTION_GENERIC_LM_HOST = os.environ.get(
    "EAPP_ACTION_GENERIC_LM_HOST", "generic_lm"
)
EAPP_ACTION_GENERIC_LM_PORT = os.environ.get("EAPP_ACTION_GENERIC_LM_PORT", "80")
EAPP_ACTION_GENERIC_LM_KEY = os.environ.get(
    "EAPP_ACTION_GENERIC_LM_KEY", "sk-11111111111111111111111111111111"
)
EAPP_ACTION_GENERIC_LM_TYPE = os.environ.get("EAPP_ACTION_GENERIC_LM_TYPE", "")
EAPP_ACTION_GENERIC_LM_URI = (
    f"{EAPP_ACTION_GENERIC_LM_HOST}:{EAPP_ACTION_GENERIC_LM_PORT}"
)
EAPP_ACTION_GENERIC_LM_MODEL = "gpt-4o-mini"

from typing import Annotated, Literal

Operator = Literal["+", "-", "*", "/"]


from autogen import GroupChat, GroupChatManager
from google.protobuf.text_format import MessageToString
from pydantic import BaseModel


def calculator(a: int, b: int, operator: Annotated[Operator, "operator"]) -> int:
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        return int(a / b)
    else:
        raise ValueError("Invalid operator")


AAS_AUTH = AccountAssistantServicesAccessAuthDetails()
S_AUTH = SpaceServicesAccessAuthDetails()
KS_AUTH = SpaceKnowledgeServicesAccessAuthDetails()
PS_AUTH = SpaceProductServicesAccessAuthDetails()
SS_AUTH = SpaceServiceServicesAccessAuthDetails()
SKDS = []
SSDS = []
SPDS = []


def my_account() -> Account:
    return AAS_AUTH.account_assistant.account


def my_account_first_name() -> str:
    return my_account().account_first_name


def my_account_last_name() -> str:
    return my_account().account_last_name


def my_account_assistant() -> AccountAssistant:
    return AAS_AUTH.account_assistant


def my_account_id() -> str:
    return my_account().account_id


def my_account_space() -> Space:
    return S_AUTH.space


def my_account_space_id(account_id: str) -> str:
    return my_account_space().space_id


def my_account_space_knowledge() -> SpaceKnowledge:
    return KS_AUTH.space_knowledge


def my_account_space_product() -> SpaceProduct:
    return PS_AUTH.space_product


def my_account_space_service() -> SpaceService:
    return SS_AUTH.space_service


def my_account_space_knowledge_id(space_id: str) -> str:
    return my_account_space_knowledge().space_knowledge_id


def my_account_space_product_id() -> str:
    return my_account_space_product().space_product_id


def my_account_space_knowledge_domain_ids(space_knowledge_id: str) -> list:
    return [skd.space_knowledge_domain_id for skd in SKDS]


def my_account_space_knowledge_domain_name(space_knowledge_domain_id: str) -> str:
    for skd in SKDS:
        if skd.space_knowledge_domain_id == space_knowledge_domain_id:
            return skd.space_knowledge_domain_name
    return "Domain not found"


def my_account_space_product_domain_ids(space_product_id: str) -> list:
    """returns a list of uuid4 in string format wrt product domains"""
    return [spd.id for spd in SPDS]


def my_account_space_product_domain_details(space_product_domain_id: str) -> str:
    """returns serailised string of a protobuf message of space product domain"""
    for spd in SPDS:
        if spd.id == space_product_domain_id:
            return MessageToString(spd, as_one_line=True)
    return "Domain not found"


def my_account_space_product_domain_image_files(product_images_domain_id: str) -> list:
    """returns serailised string of a protobuf message of space product domain collars"""
    # get the skd
    _, _, skd = DiscoverSpaceKnowledgeConsumer.get_space_knowledge_domain_by_id(
        access_auth_details=KS_AUTH, space_knowledge_domain_id=product_images_domain_id
    )
    # get the skd auth
    skd_auth, _, _ = (
        AccessSpaceKnowledgeDomainConsumer.space_knowledge_domain_access_token(
            access_auth_details=KS_AUTH, space_knowledge_domain=skd
        )
    )
    # get all the files
    all_files_response = DiscoverSpaceKnowledgeDomainConsumer.get_all_domain_files(
        skd_auth=skd_auth
    )
    files = all_files_response.files
    # convert files into string
    fs = []
    for f in files:
        fs.append(MessageToString(f, as_one_line=True))
    return fs


def my_account_space_product_domain_image_file_download(
    product_images_domain_id: str, product_image_file_id: str
) -> list:
    """returns serailised string of a protobuf message of space knowledge domain file"""
    # get the skd
    _, _, skd = DiscoverSpaceKnowledgeConsumer.get_space_knowledge_domain_by_id(
        access_auth_details=KS_AUTH, space_knowledge_domain_id=product_images_domain_id
    )
    # get the skd auth
    skd_auth, _, _ = (
        AccessSpaceKnowledgeDomainConsumer.space_knowledge_domain_access_token(
            access_auth_details=KS_AUTH, space_knowledge_domain=skd
        )
    )
    # get the file
    file = DiscoverSpaceKnowledgeDomainFileConsumer.get_file_by_id(
        skd_auth=skd_auth, file_id=product_image_file_id
    )
    # download the file content
    file_content = DiscoverSpaceKnowledgeDomainFileConsumer.download(
        skd_auth=skd_auth, file=file
    )
    return file_content


def my_account_space_product_domain_collars(space_product_domain_id: str) -> list:
    """returns serailised string of a protobuf message of space product domain collars"""
    d = SpaceProductDomain()
    for spd in SPDS:
        if spd.id == space_product_domain_id:
            d = spd
    spd_auth, _, _ = AccessSpaceProductDomainConsumer.space_product_domain_access_token(
        access_auth_details=PS_AUTH, space_product_domain=d
    )
    cs = []
    if d.HasField("dc499999994"):
        rd = DC499999994EPME5000Consumer.list(request=spd_auth)
        for c in rd.collars:
            cs.append(MessageToString(c, as_one_line=True))
    return cs


def my_account_space_product_domain_collar(
    space_product_domain_id: str, space_product_domain_collar_id: str
) -> str:
    """returns serailised string of a protobuf message of space product domain collars"""
    d = SpaceProductDomain()
    for spd in SPDS:
        if spd.id == space_product_domain_id:
            d = spd
    spd_auth, _, _ = AccessSpaceProductDomainConsumer.space_product_domain_access_token(
        access_auth_details=PS_AUTH, space_product_domain=d
    )
    if d.HasField("dc499999994"):
        c = DC499999994EPME5000Consumer.get(
            spd_auth=spd_auth, sk_auth=KS_AUTH, c_id=space_product_domain_collar_id
        )
        return MessageToString(c, as_one_line=True)
    return "Couldn't find"


def my_account_space_product_domain_name(space_product_domain_id: str) -> str:
    for spd in SPDS:
        if spd.id == space_product_domain_id:
            return spd.name
    return "Domain not found"


def my_account_space_product_domain_collar_code(space_product_domain_id: str) -> str:
    for spd in SPDS:
        if spd.id == space_product_domain_id:
            if spd.HasField("dc499999994"):
                return "DC499999994"
    return "Domain not found"


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
    account_assistant_services_access_session_token_details: (
        PersistentSessionTokenDetailsModel
    )
    requested_at: Optional[datetime]


class AccountAssistantConnectedAccountModel(BaseModel):
    account_connection_id: str
    account_id: str
    connected_at: datetime


class SpaceKnowledgeActionModel(str, Enum):
    ASK_QUESTION = "ASK_QUESTION"


class UniverseModel(BaseModel):
    universe_id: str
    universe_created_at: datetime
    universe_name: str
    universe_description: str
    universe_updated_at: datetime


class GalaxyModel(BaseModel):
    galaxy_id: str
    galaxy_name: str
    universe: UniverseModel
    galaxy_created_at: datetime


class SpaceModel(BaseModel):
    galaxy: GalaxyModel  # Adjust the type according to the type of Galaxy
    space_id: str
    space_accessibility_type: (
        str  # Adjust the type according to the type of SpaceAccessibilityType
    )
    space_isolation_type: (
        str  # Adjust the type according to the type of SpaceIsolationType
    )
    space_entity_type: str  # Adjust the type according to the type of SpaceEntityType
    space_admin_id: str
    space_created_at: Optional[
        str
    ]  # Adjust the type according to the type of space_created_at


class SpaceKnowledgeModel(BaseModel):
    space_knowledge_name: str
    space_knowledge_id: str
    space_knowledge_admin_account_id: str
    space: SpaceModel  # Adjust the type according to the type of space
    created_at: datetime  # Adjust the type according to the type of created_at


class SpaceKnowledgeDomainCollarEnumModel(str, Enum):
    WHITE_COLLAR = "WHITE_COLLAR"
    BLUE_COLLAR = "BLUE_COLLAR"
    PINK_COLLAR = "PINK_COLLAR"
    GOLD_COLLAR = "GOLD_COLLAR"
    RED_COLLAR = "RED_COLLAR"
    PURPLE_COLLAR = "PURPLE_COLLAR"
    NEW_COLLAR = "NEW_COLLAR"
    NO_COLLAR = "NO_COLLAR"
    ORANGE_COLLAR = "ORANGE_COLLAR"
    GREEN_COLLAR = "GREEN_COLLAR"
    SCARLET_COLLAR = "SCARLET_COLLAR"
    BROWN_COLLAR = "BROWN_COLLAR"
    STEEL_COLLAR = "STEEL_COLLAR"
    BLACK_COLLAR = "BLACK_COLLAR"
    GREY_COLLAR = "GREY_COLLAR"
    SKD_I_AM_COLLAR = "SKD_I_AM_COLLAR"


class SpaceKnowledgeDomainModel(BaseModel):
    space_knowledge_domain_id: str
    space_knowledge_domain_name: str
    space_knowledge_domain_description: str
    space_knowledge_domain_collar_enum: SpaceKnowledgeDomainCollarEnumModel
    space_knowledge_domain_isolated: bool
    space_knowledge: (
        SpaceKnowledgeModel  # Adjust the type according to the type of space_knowledge
    )
    created_at: Optional[str]  # Adjust the type according to the type of created_at
    last_updated_at: Optional[
        str
    ]  # Adjust the type according to the type of last_updated_at


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
                "api_key": f"{EAPP_ACTION_GENERIC_LM_KEY}",
            }
        ]
        # conf = {"config_list": [
        #     {
        #         "model": "gpt-3.5-turbo",
        #         "api_key": "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",
        #     }
        # ]}

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
            if "tool_responses" in item:
                # Get the first 'tool_responses' item
                tool_responses = item["tool_responses"][0]
                # Return the value for the key 'content'
                return tool_responses.get("content")

        # 'tool_responses' not found in chat_history
        return None

    @staticmethod
    def get_answer(
        input: Annotated[ActOnAccountMessageRequestModel, "Process an incoming request"]
    ):
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
                        account_personal_email_id=input.access_auth_details.account_assistant.account.account_personal_email_id,
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
                                big_bang_at=input.space_knowledge_domain.space_knowledge.space.galaxy.universe.big_bang_at,
                            ),
                        ),
                    ),
                ),
            ),
            act_on_particular_domain=input.act_on_particular_domain,
        )
        logging.info(f"get_answer: input: {input}")
        if input.act_on_particular_domain:
            _, _, domains_ranked_answers = SpaceKnowledgeActionConsumer().ask_question(
                access_auth_details=request.access_auth_details,
                message=input.message,
                ask_particular_domain=True,
                space_knowledge_domain=request.space_knowledge_domain,
            )
        else:
            _, _, domains_ranked_answers = SpaceKnowledgeActionConsumer().ask_question(
                access_auth_details=request.access_auth_details,
                message=input.message,
                ask_particular_domain=False,
                space_knowledge_domain=SpaceKnowledgeDomain(),
            )
        for domain_ranked_answer in domains_ranked_answers:
            print(
                f"{'-' * 20}{domain_ranked_answer.space_knowledge_domain.space_knowledge_domain_name}{'-' * 20}"
            )
            for ranked_answer in domain_ranked_answer.ranked_answers:
                print(f"\t>{ranked_answer.para_rank}>>>{ranked_answer.answer}")
        message_sources = []
        msg, space_id, space_type_id, domain_id, context_id = (
            ActionAccountAssistantService.resolve_best_answer(domains_ranked_answers)
        )
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
        validation_done, validation_message = (
            access_consumer.validate_account_assistant_services(
                request.access_auth_details
            )
        )
        AtlasTracer.set_span_attr("valid", validation_done)
        if validation_done is False:
            return ResponseMeta(
                meta_done=validation_done, meta_message=validation_message
            )
        else:
            should_continue = True
            should_assist = False
            if request.space_knowledge_action == 0 and should_continue:
                # agent = ConversableAgent(
                #     "chatbot",
                #     llm_config=self.llm_config,
                #     code_execution_config=False,  # Turn off code execution, by default it is off.
                #     function_map=None,  # No registered functions, by default it is None.
                #     human_input_mode="NEVER",  # Never ask for human input.
                # )

                global AAS_AUTH
                global S_AUTH
                global KS_AUTH
                global PS_AUTH
                global SS_AUTH
                global SKDS
                global SPDS
                global SSDS

                logging.info(f"access_auth_details: {request.access_auth_details}")

                AAS_AUTH = request.access_auth_details
                _, _, S_AUTH = AccessSpaceConsumer.assist_space_access_token(AAS_AUTH)
                _, _, KS_AUTH = (
                    AccessSpaceKnowledgeConsumer.space_knowledge_access_token(S_AUTH)
                )
                _, _, PS_AUTH = AccessSpaceProductConsumer.space_product_access_token(
                    S_AUTH
                )
                _, _, SS_AUTH = AccessSpaceServiceConsumer.space_service_access_token(
                    S_AUTH
                )

                _, _, SKDS = DiscoverSpaceKnowledgeConsumer.get_space_knowledge_domains(
                    KS_AUTH
                )
                _, _, SPDS = DiscoverSpaceProductConsumer.get_space_product_domains(
                    PS_AUTH
                )

                _, _, SSDS = DiscoverSpaceServiceConsumer.get_space_service_domains(
                    SS_AUTH
                )

                assistant_agent = ConversableAgent(
                    name="Ethos_Assistant",
                    system_message="You are a helpful AI assistant. "
                    "You can help with simple calculations. "
                    "Return 'TERMINATE' when the task is done.",
                    llm_config=self.llm_config,
                )
                my_space_agent = ConversableAgent(
                    name="Space_Assistant",
                    system_message="You are a helpful Ethos Space assistant. "
                    "You can help with simple discovery about space details. "
                    "Each account space may have four kinds of spaces - "
                    "Knowledge Space, Product Space, Service Space, Things Space. "
                    "Each kind of space may have multiple contextual domains."
                    "Knowledge domains are to share or discover information, "
                    "Product domains are to buy or sell prodcuts, "
                    "Service domains are to do or get work, "
                    "Things domains are to control inbound or outbound of anything."
                    "Return 'TERMINATE' when the task is done.",
                    llm_config=self.llm_config,
                )
                my_space_knowledge_agent = ConversableAgent(
                    name="Space_Knowledge_Assistant",
                    system_message="You are a helpful Ethos Space Knowledge assistant. "
                    "You can help with simple discovery about space knowledge details. "
                    "Knowledge domains are to share or discover information"
                    "Return 'TERMINATE' when the task is done.",
                    llm_config=self.llm_config,
                )
                my_space_product_agent = MultimodalConversableAgent(
                    name="Space_Product_Assistant",
                    system_message="You are a helpful Ethos Space Product assistant. "
                    "You can help with simple discovery about space product details. "
                    "Product domains are to buy or sell prodcuts, "
                    "SpaceProduct has these parameters 1. string space_product_name"
                    " 2. string space_product_id, 3. string space_product_admin_account_id"
                    " 4. Space space, 5. google.protobuf.Timestamp created_at. "
                    "SpaceProductDomain has these parameters 1. string id, 2. string name"
                    " 3. string description, 4. bool is_isolated, 5. elint.entity.SpaceProduct "
                    "space_product, 6. google.protobuf.Timestamp created_at, 7. google.protobuf.Timestamp last_updated_at"
                    " 8. oneof collar { elint.collars.DC499999994 dc499999994 = 499999994 }"
                    "Return 'TERMINATE' when the task is done.",
                    llm_config=self.llm_config,
                )

                my_space_service_agent = ConversableAgent(
                    name="Space_Knowledge_Assistant",
                    system_message="You are a helpful Ethos Space Knowledge assistant. "
                    "You can help with simple discovery about space service details. "
                    "Service domains are to do or get work, "
                    "Return 'TERMINATE' when the task is done.",
                    llm_config=self.llm_config,
                )

                user_proxy_agent = ConversableAgent(
                    "User",
                    llm_config=False,
                    is_termination_msg=lambda msg: msg.get("content") is not None
                    and "TERMINATE" in msg["content"],
                    human_input_mode="NEVER",
                )

                my_space_agent.description = "Ethos Account Space Assistant"
                my_space_knowledge_agent.description = (
                    "Ethos Account Space Knowledge Assistant"
                )
                my_space_service_agent.description = (
                    "Ethos Account Space Service Assistant"
                )
                my_space_product_agent.description = (
                    "Ethos Account Space Product Assistant"
                )

                # Register the tool signature with the assistant agent.
                assistant_agent.register_for_llm(
                    name="calculator", description="A simple calculator"
                )(calculator)

                my_space_agent.register_for_llm(
                    name="my_account_first_name",
                    description="A simple account details fetcher of first name",
                )(my_account_first_name)
                my_space_agent.register_for_llm(
                    name="my_account_last_name",
                    description="A simple account details fetcher of last name",
                )(my_account_last_name)
                my_space_agent.register_for_llm(
                    name="my_account_id",
                    description="A simple account details fetcher of id",
                )(my_account_id)
                my_space_agent.register_for_llm(
                    name="my_account_space_id",
                    description="A simple account space details fetcher of id",
                )(my_account_space_id)

                my_space_knowledge_agent.register_for_llm(
                    name="my_account_space_knowledge_id",
                    description="A simple account space knowledge details fetcher of id",
                )(my_account_space_knowledge_id)
                my_space_knowledge_agent.register_for_llm(
                    name="my_account_space_knowledge_domain_ids",
                    description="A simple account space knowledge details fetcher of domain ids",
                )(my_account_space_knowledge_domain_ids)
                my_space_knowledge_agent.register_for_llm(
                    name="my_account_space_knowledge_domain_name",
                    description="A simple account space knowledge domain details fetcher of name",
                )(my_account_space_knowledge_domain_name)

                my_space_product_agent.register_for_llm(
                    name="my_account_space_product_id",
                    description="A simple account space product details fetcher of id",
                )(my_account_space_product_id)
                my_space_product_agent.register_for_llm(
                    name="my_account_space_product_domain_ids",
                    description="A simple account space product details fetcher of domain ids",
                )(my_account_space_product_domain_ids)
                my_space_product_agent.register_for_llm(
                    name="my_account_space_product_domain_details",
                    description="A simple account space product domain details fetcher of all details by domain id",
                )(my_account_space_product_domain_details)
                my_space_product_agent.register_for_llm(
                    name="my_account_space_product_domain_collars",
                    description="A simple account space product domain collar list fetcher of all collar details by domain id",
                )(my_account_space_product_domain_collars)
                my_space_product_agent.register_for_llm(
                    name="my_account_space_product_domain_collar",
                    description="A simple account space product domain collar details fetcher by domain id and collar id",
                )(my_account_space_product_domain_collar)
                my_space_product_agent.register_for_llm(
                    name="my_account_space_product_domain_image_files",
                    description="A simple account space product domain collar dc499999994 details fetcher of all product images fetcher by product images domain id",
                )(my_account_space_product_domain_image_files)
                my_space_product_agent.register_for_llm(
                    name="my_account_space_product_domain_image_file_download",
                    description="A simple account space product domain collar dc499999994 details fetcher of single image content fetcher by product images domain id and image file id",
                )(my_account_space_product_domain_image_file_download)

                # my_space_product_agent.register_for_llm(
                #     name="my_account_space_product_domain_name",
                #     description="A simple account space product domain details fetcher of name by domain id",
                # )(my_account_space_product_domain_name)
                # my_space_product_agent.register_for_llm(
                #     name="my_account_space_product_domain_collar_code",
                #     description="A simple account space product domain details fetcher of collar code by domain id",
                # )(my_account_space_product_domain_collar_code)

                # Register the tool function with the user proxy agent.
                user_proxy_agent.register_for_execution(name="calculator")(calculator)
                user_proxy_agent.register_for_execution(name="my_account_first_name")(
                    my_account_first_name
                )
                user_proxy_agent.register_for_execution(name="my_account_id")(
                    my_account_id
                )
                user_proxy_agent.register_for_execution(name="my_account_space_id")(
                    my_account_space_id
                )

                user_proxy_agent.register_for_execution(
                    name="my_account_space_knowledge_id"
                )(my_account_space_knowledge_id)
                user_proxy_agent.register_for_execution(
                    name="my_account_space_knowledge_domain_ids"
                )(my_account_space_knowledge_domain_ids)
                user_proxy_agent.register_for_execution(
                    name="my_account_space_knowledge_domain_name"
                )(my_account_space_knowledge_domain_name)

                user_proxy_agent.register_for_execution(
                    name="my_account_space_product_id"
                )(my_account_space_product_id)
                user_proxy_agent.register_for_execution(
                    name="my_account_space_product_domain_ids"
                )(my_account_space_product_domain_ids)
                user_proxy_agent.register_for_execution(
                    name="my_account_space_product_domain_details"
                )(my_account_space_product_domain_details)
                user_proxy_agent.register_for_execution(
                    name="my_account_space_product_domain_collars"
                )(my_account_space_product_domain_collars)
                user_proxy_agent.register_for_execution(
                    name="my_account_space_product_domain_collar"
                )(my_account_space_product_domain_collar)
                user_proxy_agent.register_for_execution(
                    name="my_account_space_product_domain_image_files"
                )(my_account_space_product_domain_image_files)
                user_proxy_agent.register_for_execution(
                    name="my_account_space_product_domain_image_file_download"
                )(my_account_space_product_domain_image_file_download)

                # Domain ID: 9DF72AAA-1719-4246-B59B-0D1AF20DC71A
                # Collar ID: FA124208-8EB0-4EAA-92F9-72005A062CFB

                # what are the details of collar FA124208-8EB0-4EAA-92F9-72005A062CFB in domain 9DF72AAA-1719-4246-B59B-0D1AF20DC71A, and what details about their images you know? can you download the content of the first image?

                # user_proxy_agent.register_for_execution(
                #     name="my_account_space_product_domain_name"
                # )(my_account_space_product_domain_name)
                # user_proxy_agent.register_for_execution(
                #     name="my_account_space_product_domain_collar_code"
                # )(my_account_space_product_domain_collar_code)

                # Assuming `request` is an instance of ActOnAccountMessageRequest
                # assistant_agent.register_for_llm(
                #     name="ask_question", description="A question answering system"
                # )(ActionAccountAssistantService.get_answer_function)
                # user_proxy_agent.register_for_execution(name="ask_question")(
                #     ActionAccountAssistantService.get_answer_function
                # )
                # reply = agent.generate_reply(
                #     messages=[{"content": request.message, "role": "user"}]
                # )

                # working one
                chat_result = user_proxy_agent.initiate_chat(
                    my_space_product_agent,
                    message=request.message,
                    max_turns=20,
                    summary_method="reflection_with_llm",
                )

                # # new one
                # group_chat = GroupChat(
                #     agents=[
                #         user_proxy_agent,
                #         my_space_agent,
                #         my_space_knowledge_agent,
                #         my_space_product_agent,
                #     ],
                #     messages=[],
                #     max_round=6,
                # )

                # group_chat_manager = GroupChatManager(
                #     groupchat=group_chat,
                #     llm_config=self.llm_config,
                # )

                # chat_result = user_proxy_agent.initiate_chat(
                #     group_chat_manager,
                #     message=request.message,
                #     summary_method="reflection_with_llm",
                # )

                logging.info(f"chat_result: {chat_result}")
                # msg, space_id, space_type_id, domain_id, context_id, message_sources = (
                #     self.get_tool_response_content(chat_result)
                # )
                response = send_message_to_account(
                    access_auth_details=request.access_auth_details,
                    connected_account=request.connected_account,
                    message=chat_result.summary,
                    message_source_space_id="space_id",
                    message_source_space_type_id="space_type_id",
                    message_source_space_domain_id="domain_id",
                    message_source_space_domain_action=SpaceKnowledgeAction.ASK_QUESTION,
                    message_source_space_domain_action_context_id="context_id",
                    message_source=[],
                )
                return ResponseMeta(
                    meta_done=validation_done, meta_message=validation_message
                )
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
                    "Authorization": f"Bearer {EAPP_ACTION_GENERIC_LM_KEY}",
                }
                data = {
                    "model": f"{EAPP_ACTION_GENERIC_LM_TYPE}",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are Ethosai. Your. Personal. Conversational. Self learning. Distributed. "
                            "Intelligent. Assistant.",
                        },
                        {"role": "user", "content": f"{request.message}"},
                    ],
                }

                response = requests.post(url, json=data, headers=headers)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    logging.info("API call successful!")
                    logging.info("Response:")
                    logging.info(response.json())
                    message = response.json()["choices"][0]["message"]["content"]
                else:
                    logging.info(
                        f"API call failed with status code {response.status_code}"
                    )
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
                    message_source=[],
                )
                return ResponseMeta(
                    meta_done=validation_done, meta_message=validation_message
                )
            else:
                return ResponseMeta(
                    meta_done=False, meta_message="Invalid Action Requested."
                )

    @staticmethod
    def resolve_best_answer(
        domains_ranked_answers: [DomainRankedAnswers],
    ) -> (str, str, str, str, str):
        """returns params for the first best answer for the first found domain else empty tuple"""
        message = "I couldn't find any answers in any page in the space."
        message_source_space_knowledge_domain = None
        source_ranked_answer = ""
        for domain_ranked_answer in domains_ranked_answers:
            for ranked_answer in domain_ranked_answer.ranked_answers:
                message = ranked_answer.answer
                source_ranked_answer = ranked_answer
                message_source_space_knowledge_domain = (
                    domain_ranked_answer.space_knowledge_domain
                )
                break
        if message_source_space_knowledge_domain is None:
            message_source_space_id = ""
            message_source_space_type_id = ""
            message_source_space_domain_id = ""
            message_source_space_domain_action_context_id = ""
        else:
            message_source_space_id = (
                message_source_space_knowledge_domain.space_knowledge.space.space_id
            )
            message_source_space_type_id = (
                message_source_space_knowledge_domain.space_knowledge.space_knowledge_id
            )
            message_source_space_domain_id = (
                message_source_space_knowledge_domain.space_knowledge_domain_id
            )
            message_source_space_domain_action_context_id = (
                source_ranked_answer.context_id
            )
        return (
            message,
            message_source_space_id,
            message_source_space_type_id,
            message_source_space_domain_id,
            message_source_space_domain_action_context_id,
        )


# find the action
# send the request to particular action
# wait for the action response
# send account assistant message
# wait for the action response
# send account assistant message
