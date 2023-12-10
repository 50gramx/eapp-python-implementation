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

import cv2
from pytesseract import pytesseract, Output

# ethos_oem_psm_config = r'--tessdata-dir "/content/tessdata" -l eng --oem 1 --psm 12 --user_words_suffix "user_words"'
from ethos.elint.entities.space_knowledge_domain_file_page_pb2 import SpaceKnowledgeDomainFilePage
from support.data_store import DataStore

ethos_oem_psm_config = r'--oem 1 --psm 12'


def get_image_paragraphs(image_path: str):
    list_of_blocks = []
    for block_contour, block_image in get_image_blocks(image_path):
        list_of_blocks.append((block_contour, block_image))
    sorted_list_of_blocks = sorted(list_of_blocks, key=lambda block: block[0]['y'], reverse=False)

    y_max = sorted_list_of_blocks[-1][0]['y']
    if 2800 > y_max > 2100:
        # divide the page in four para
        first_para_index = 0
        second_para_index = 0
        third_para_index = 0
        fourth_para_index = len(sorted_list_of_blocks) - 1
        # fetch the block id for four para
        for block_id, block in enumerate(sorted_list_of_blocks):
            if block[0]['y'] < (y_max / 4):
                first_para_index = block_id
            elif block[0]['y'] < ((y_max / 4) * 2):
                second_para_index = block_id
            elif block[0]['y'] < ((y_max / 4) * 3):
                third_para_index = block_id
        # fetch the text for four para
        first_para_text = list()
        second_para_text = list()
        third_para_text = list()
        fourth_para_text = list()
        for i in range(0, first_para_index + 1):
            first_para_text.append(get_image_texts(sorted_list_of_blocks[i][1]))
        for i in range(first_para_index + 1, second_para_index + 1):
            second_para_text.append(get_image_texts(sorted_list_of_blocks[i][1]))
        for i in range(second_para_index + 1, third_para_index + 1):
            third_para_text.append(get_image_texts(sorted_list_of_blocks[i][1]))
        for i in range(third_para_index + 1, fourth_para_index + 1):
            fourth_para_text.append(get_image_texts(sorted_list_of_blocks[i][1]))
        first_para_text = ' '.join(first_para_text).replace('\n', '').replace('\t', '')
        second_para_text = ' '.join(second_para_text).replace('\n', '').replace('\t', '')
        third_para_text = ' '.join(third_para_text).replace('\n', '').replace('\t', '')
        fourth_para_text = ' '.join(fourth_para_text).replace('\n', '').replace('\t', '')
        # fetch the bounding box for four para
        first_para_contour_dims = {'x': 10e9, 'y': 10e9, 'w': 0, 'h': 0}
        second_para_contour_dims = {'x': 10e9, 'y': 10e9, 'w': 0, 'h': 0}
        third_para_contour_dims = {'x': 10e9, 'y': 10e9, 'w': 0, 'h': 0}
        fourth_para_contour_dims = {'x': 10e9, 'y': 10e9, 'w': 0, 'h': 0}
        for block in sorted_list_of_blocks[0:first_para_index]:
            if int(block[0]['x']) < first_para_contour_dims['x']:
                first_para_contour_dims['x'] = int(block[0]['x'])
            if int(block[0]['y']) < first_para_contour_dims['y']:
                first_para_contour_dims['y'] = int(block[0]['y'])
            if (int(block[0]['x']) + int(block[0]['w'])) > first_para_contour_dims['w']:
                first_para_contour_dims['w'] = int(block[0]['x']) + int(block[0]['w'])
            if (int(block[0]['y']) + int(block[0]['h'])) > first_para_contour_dims['h']:
                first_para_contour_dims['h'] = int(block[0]['y']) + int(block[0]['h'])
        for block in sorted_list_of_blocks[first_para_index + 1: second_para_index]:
            if int(block[0]['x']) < second_para_contour_dims['x']:
                second_para_contour_dims['x'] = int(block[0]['x'])
            if int(block[0]['y']) < second_para_contour_dims['y']:
                second_para_contour_dims['y'] = int(block[0]['y'])
            if (int(block[0]['x']) + int(block[0]['w'])) > second_para_contour_dims['w']:
                second_para_contour_dims['w'] = int(block[0]['x']) + int(block[0]['w'])
            if (int(block[0]['y']) + int(block[0]['h'])) > second_para_contour_dims['h']:
                second_para_contour_dims['h'] = int(block[0]['y']) + int(block[0]['h'])
        for block in sorted_list_of_blocks[second_para_index + 1: third_para_index]:
            if int(block[0]['x']) < third_para_contour_dims['x']:
                third_para_contour_dims['x'] = int(block[0]['x'])
            if int(block[0]['y']) < third_para_contour_dims['y']:
                third_para_contour_dims['y'] = int(block[0]['y'])
            if (int(block[0]['x']) + int(block[0]['w'])) > third_para_contour_dims['w']:
                third_para_contour_dims['w'] = int(block[0]['x']) + int(block[0]['w'])
            if (int(block[0]['y']) + int(block[0]['h'])) > third_para_contour_dims['h']:
                third_para_contour_dims['h'] = int(block[0]['y']) + int(block[0]['h'])
        for block in sorted_list_of_blocks[third_para_index + 1: fourth_para_index]:
            if int(block[0]['x']) < fourth_para_contour_dims['x']:
                fourth_para_contour_dims['x'] = int(block[0]['x'])
            if int(block[0]['y']) < fourth_para_contour_dims['y']:
                fourth_para_contour_dims['y'] = int(block[0]['y'])
            if (int(block[0]['x']) + int(block[0]['w'])) > fourth_para_contour_dims['w']:
                fourth_para_contour_dims['w'] = int(block[0]['x']) + int(block[0]['w'])
            if (int(block[0]['y']) + int(block[0]['h'])) > fourth_para_contour_dims['h']:
                fourth_para_contour_dims['h'] = int(block[0]['y']) + int(block[0]['h'])
        return [(first_para_contour_dims, first_para_text), (second_para_contour_dims, second_para_text),
                (third_para_contour_dims, third_para_text), (fourth_para_contour_dims, fourth_para_text)]
    elif 2100 > y_max > 1400:
        # divide the page in three para
        first_para_index = 0
        second_para_index = 0
        third_para_index = len(sorted_list_of_blocks) - 1
        # fetch the block id for three para
        for block_id, block in enumerate(sorted_list_of_blocks):
            if block[0]['y'] < (y_max / 3):
                first_para_index = block_id
            elif block[0]['y'] < ((y_max / 3) * 2):
                second_para_index = block_id
        # fetch the text for three para
        first_para_text = list()
        second_para_text = list()
        third_para_text = list()
        for i in range(0, first_para_index + 1):
            first_para_text.append(get_image_texts(sorted_list_of_blocks[i][1]))
        for i in range(first_para_index + 1, second_para_index + 1):
            second_para_text.append(get_image_texts(sorted_list_of_blocks[i][1]))
        for i in range(second_para_index + 1, third_para_index + 1):
            third_para_text.append(get_image_texts(sorted_list_of_blocks[i][1]))
        first_para_text = ' '.join(first_para_text).replace('\n', '').replace('\t', '')
        second_para_text = ' '.join(second_para_text).replace('\n', '').replace('\t', '')
        third_para_text = ' '.join(third_para_text).replace('\n', '').replace('\t', '')
        # fetch the bounding box for three para
        first_para_contour_dims = {'x': 10e9, 'y': 10e9, 'w': 0, 'h': 0}
        second_para_contour_dims = {'x': 10e9, 'y': 10e9, 'w': 0, 'h': 0}
        third_para_contour_dims = {'x': 10e9, 'y': 10e9, 'w': 0, 'h': 0}
        for block in sorted_list_of_blocks[0:first_para_index]:
            if int(block[0]['x']) < first_para_contour_dims['x']:
                first_para_contour_dims['x'] = int(block[0]['x'])
            if int(block[0]['y']) < first_para_contour_dims['y']:
                first_para_contour_dims['y'] = int(block[0]['y'])
            if (int(block[0]['x']) + int(block[0]['w'])) > first_para_contour_dims['w']:
                first_para_contour_dims['w'] = int(block[0]['x']) + int(block[0]['w'])
            if (int(block[0]['y']) + int(block[0]['h'])) > first_para_contour_dims['h']:
                first_para_contour_dims['h'] = int(block[0]['y']) + int(block[0]['h'])
        for block in sorted_list_of_blocks[first_para_index + 1: second_para_index]:
            if int(block[0]['x']) < second_para_contour_dims['x']:
                second_para_contour_dims['x'] = int(block[0]['x'])
            if int(block[0]['y']) < second_para_contour_dims['y']:
                second_para_contour_dims['y'] = int(block[0]['y'])
            if (int(block[0]['x']) + int(block[0]['w'])) > second_para_contour_dims['w']:
                second_para_contour_dims['w'] = int(block[0]['x']) + int(block[0]['w'])
            if (int(block[0]['y']) + int(block[0]['h'])) > second_para_contour_dims['h']:
                second_para_contour_dims['h'] = int(block[0]['y']) + int(block[0]['h'])
        for block in sorted_list_of_blocks[second_para_index + 1: third_para_index]:
            if int(block[0]['x']) < third_para_contour_dims['x']:
                third_para_contour_dims['x'] = int(block[0]['x'])
            if int(block[0]['y']) < third_para_contour_dims['y']:
                third_para_contour_dims['y'] = int(block[0]['y'])
            if (int(block[0]['x']) + int(block[0]['w'])) > third_para_contour_dims['w']:
                third_para_contour_dims['w'] = int(block[0]['x']) + int(block[0]['w'])
            if (int(block[0]['y']) + int(block[0]['h'])) > third_para_contour_dims['h']:
                third_para_contour_dims['h'] = int(block[0]['y']) + int(block[0]['h'])
        return [(first_para_contour_dims, first_para_text), (second_para_contour_dims, second_para_text),
                (third_para_contour_dims, third_para_text)]
    elif 1400 > y_max > 700:
        # divide the page in two para
        first_para_index = 0
        second_para_index = len(sorted_list_of_blocks) - 1
        # fetch the block id for two para
        for block_id, block in enumerate(sorted_list_of_blocks):
            if block[0]['y'] < (y_max / 2):
                first_para_index = block_id
        # fetch the text for two para
        first_para_text = list()
        second_para_text = list()
        for i in range(0, first_para_index + 1):
            first_para_text.append(get_image_texts(sorted_list_of_blocks[i][1]))
        for i in range(first_para_index + 1, second_para_index + 1):
            second_para_text.append(get_image_texts(sorted_list_of_blocks[i][1]))
        first_para_text = ' '.join(first_para_text).replace('\n', '').replace('\t', '')
        second_para_text = ' '.join(second_para_text).replace('\n', '').replace('\t', '')
        # fetch the bounding box for two para
        first_para_contour_dims = {'x': 10e9, 'y': 10e9, 'w': 0, 'h': 0}
        second_para_contour_dims = {'x': 10e9, 'y': 10e9, 'w': 0, 'h': 0}
        for block in sorted_list_of_blocks[0:first_para_index]:
            if int(block[0]['x']) < first_para_contour_dims['x']:
                first_para_contour_dims['x'] = int(block[0]['x'])
            if int(block[0]['y']) < first_para_contour_dims['y']:
                first_para_contour_dims['y'] = int(block[0]['y'])
            if (int(block[0]['x']) + int(block[0]['w'])) > first_para_contour_dims['w']:
                first_para_contour_dims['w'] = int(block[0]['x']) + int(block[0]['w'])
            if (int(block[0]['y']) + int(block[0]['h'])) > first_para_contour_dims['h']:
                first_para_contour_dims['h'] = int(block[0]['y']) + int(block[0]['h'])
        for block in sorted_list_of_blocks[first_para_index + 1: second_para_index]:
            if int(block[0]['x']) < second_para_contour_dims['x']:
                second_para_contour_dims['x'] = int(block[0]['x'])
            if int(block[0]['y']) < second_para_contour_dims['y']:
                second_para_contour_dims['y'] = int(block[0]['y'])
            if (int(block[0]['x']) + int(block[0]['w'])) > second_para_contour_dims['w']:
                second_para_contour_dims['w'] = int(block[0]['x']) + int(block[0]['w'])
            if (int(block[0]['y']) + int(block[0]['h'])) > second_para_contour_dims['h']:
                second_para_contour_dims['h'] = int(block[0]['y']) + int(block[0]['h'])
        return [(first_para_contour_dims, first_para_text), (second_para_contour_dims, second_para_text)]
    else:
        # don't divide the page in para, instead return the whole page as one para
        first_para_index = len(sorted_list_of_blocks) - 1
        # fetch the text for one para
        first_para_text = list()
        for i in range(0, first_para_index + 1):
            first_para_text.append(get_image_texts(sorted_list_of_blocks[i][1]))
        first_para_text = ' '.join(first_para_text).replace('\n', '').replace('\t', '')
        # fetch the bounding box for two para
        first_para_contour_dims = {'x': 10e9, 'y': 10e9, 'w': 0, 'h': 0}
        for block in sorted_list_of_blocks[0:first_para_index]:
            if int(block[0]['x']) < first_para_contour_dims['x']:
                first_para_contour_dims['x'] = int(block[0]['x'])
            if int(block[0]['y']) < first_para_contour_dims['y']:
                first_para_contour_dims['y'] = int(block[0]['y'])
            if (int(block[0]['x']) + int(block[0]['w'])) > first_para_contour_dims['w']:
                first_para_contour_dims['w'] = int(block[0]['x']) + int(block[0]['w'])
            if (int(block[0]['y']) + int(block[0]['h'])) > first_para_contour_dims['h']:
                first_para_contour_dims['h'] = int(block[0]['y']) + int(block[0]['h'])
        return [(first_para_contour_dims, first_para_text)]


def get_image_blocks(image_path: str):
    # Load image, grayscale, Gaussian blur, Otsu's threshold
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Create rectangular structuring element and dilate
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    # Find contours and draw rectangle
    contours = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    page_contour_dims = ["x", "y", "w", "h"]
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)    # to draw para borders
        yield dict(zip(page_contour_dims, [x, y, w, h])), image[y:y + h, x:x + w]


def get_page_image_text(page: SpaceKnowledgeDomainFilePage):
    data_store_client = DataStore()
    data_store_client.download_space_knowledge_domain_file_page(page)
    page_image = cv2.imread(data_store_client.get_tmp_page_filepath(page=page))
    page_texts = get_image_texts(page_image)
    data_store_client.delete_tmp_page(page=page)
    return page_texts


def get_image_texts(image):
    extracted_image_data = get_image_data(image)
    return process_extracted_image_data_texts(extracted_image_data)


def get_image_data(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return pytesseract.image_to_data(image_rgb, output_type=Output.DICT, config=ethos_oem_psm_config)


def process_extracted_image_data_texts(results):
    # print("-"*30)
    # print(get_page_text(results))
    # print("-" * 30)
    # trailing_blanks_list = []
    # page_text = list()
    # for i in range(0, len(results["text"])):
    #     text = results["text"][i]
    #     text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
    #     # if text != '' and len(trailing_blanks_list) == 0:
    #     #     page_text.append(fr'{text}')
    #     # elif (len(trailing_blanks_list) == 0) or (len(trailing_blanks_list) > 0 and text == ''):
    #     #     trailing_blanks_list.append(text)
    #     # elif len(trailing_blanks_list) > 0 and text != '':
    #     #     if len(trailing_blanks_list) == 1:
    #     #         page_text.append(fr'[SEP]')
    #     #     else:
    #     #         page_text.extend([fr'{trailing_blanks}' for trailing_blanks in trailing_blanks_list[:-2]])
    #     #         page_text.append([fr'[PARA]', fr'[SEP]'])
    #     #     trailing_blanks_list = []
    #     #     page_text.append(fr'{text}')
    #     page_text.append(text)
    # print('*'*30)
    # print(page_text)
    # print('*' * 30)
    # joined_page_text = ' '.join(page_text)
    # joined_page_text = joined_page_text.replace('[SEP]', '').replace('[PARA]', '')
    return get_page_text(results)


def get_page_text(results):
    trailing_blanks_list = []
    next_line = None
    page_text = list()
    # last_line = None
    for i in range(0, len(results["text"])):
        text = results["text"][i]
        # conf = int(results["conf"][i])
        text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
        # pp.pprint(fr'{text}')
        if text != '' and len(trailing_blanks_list) == 0:
            page_text.append(fr'{text}')
            # pp.pprint(fr'{text}')
        elif len(trailing_blanks_list) == 0:
            trailing_blanks_list.append(text)
        elif len(trailing_blanks_list) > 0 and text == '':
            trailing_blanks_list.append(text)
        elif len(trailing_blanks_list) > 0 and text != '':
            if len(trailing_blanks_list) == 1:
                page_text.append(fr'[SEP]')
                # pp.pprint(fr'[SEP]')
            else:
                for trailing_blanks in trailing_blanks_list[:-2]:
                    page_text.append(fr'{trailing_blanks}')
                    # pp.pprint(fr'{trailing_blanks}')
                page_text.append(fr'[PARA]')
                page_text.append(fr'[SEP]')
                # pp.pprint(fr'[PARA]')
                # pp.pprint(fr'[SEP]')
            trailing_blanks_list = []
            page_text.append(fr'{text}')
            # pp.pprint(fr'{text}')
    return ' '.join(page_text).replace('[SEP]', '\n\t').replace('[PARA]', '\t')
