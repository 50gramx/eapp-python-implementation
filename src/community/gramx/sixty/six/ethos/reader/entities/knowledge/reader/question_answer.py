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

import logging

import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering


class QuestionAnswer:
    """ A python singleton """

    class __impl:
        """ Implementation of the singleton interface """

        def __init__(self):
            """
            Let's use the general pre-trained bert base on general dump of english cased text trained on squad dataset
            Later on we'll figure a way out to do pre-training for specific domain and even later, we'll figure a way
            out to do pre-training for each author resulting to optimum understanding of author's perspective and
            author's way of reading and writing.
            """
            self.tokenizer = AutoTokenizer.from_pretrained("deepset/bert-base-cased-squad2")
            self.model = AutoModelForQuestionAnswering.from_pretrained("deepset/bert-base-cased-squad2")

        def get_page_answer(self, question: str, page_text: str) -> str:
            inputs = self.tokenizer.encode_plus(question.replace('?', ''), f"""{page_text}""", return_tensors="pt")
            logging.info(f"type(inputs): {type(inputs)}")

            answer_start_scores, answer_end_scores = self.model(**inputs)

            answer_start = torch.argmax(answer_start_scores)
            answer_end = torch.argmax(answer_end_scores) + 1

            answer = self.tokenizer.convert_tokens_to_string(
                self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end])
            ).replace('[CLS]', '')

            return answer

        def get_para_answer(self, question: str, para_text: str) -> str:
            inputs = self.tokenizer.encode_plus(question.replace('?', ''), para_text[:500], return_tensors="pt")
            logging.info(f"type(inputs): {type(inputs)}")

            answer_start_scores, answer_end_scores = self.model(**inputs)
            output = self.model(**inputs)

            logging.info(f"output: {output}, type: {type(output)}")
            logging.info(f"answer_start_scores: {answer_start_scores}, type: {type(answer_start_scores)}")
            logging.info(f"answer_start_scores: {answer_end_scores}, type: {type(answer_end_scores)}")

            answer_start = torch.argmax(answer_start_scores)
            answer_end = torch.argmax(answer_end_scores) + 1

            answer = self.tokenizer.convert_tokens_to_string(
                self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end])
            ).replace('[CLS]', '')

            if answer.find('[SEP]') > -1:
                answer = answer[answer.find('[SEP]') + 5:]

            return answer

    # storage for the instance reference
    __instance = None

    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if QuestionAnswer.__instance is None:
            # Create and remember instance
            QuestionAnswer.__instance = QuestionAnswer.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_QuestionAnswer__instance'] = QuestionAnswer.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)
