from random import random
from time import sleep
import json
import os


def print_attributes(dict):
    """
         Apend the new line to dict items
         :param dict: dictionary to append  new line
         :return: list
    """
    if len(dict) == 0:
        attrList = []
    else:
        attrList = (" \n ".join("{}: {}".format(k, v) for k, v in dict.items()))
    return attrList


def sleep_time():
    seconds = random() * 1
    sleep(seconds)


def save_record_to_files(record, pathFile, create_new_file=False):
    if create_new_file:

        with open(pathFile, mode='w', newline='', encoding='utf-8') as file:
            pass


    else:
        split_tup = os.path.splitext(pathFile)
        file_name = split_tup[0]
        file_extension = split_tup[1]

        if file_extension == '.json':
            """Save an individual record to json file; set 'create_new_file' flag to 'True' to generate new file and save"""
            json_object = json.dumps(record, indent=4, ensure_ascii=False)

            with open(pathFile, mode='a+', newline='', encoding='utf-8') as file:
                file.write(json_object)


        elif file_extension == '.txt':
            with open(pathFile, mode='a+', newline='', encoding='utf-8') as file:
                for i, list_item in enumerate(record):
                    if isinstance(list_item, dict):
                        for j, key in enumerate(list_item.keys()):
                            file.write(f"{key}")
                            file.write('\n')
                            if isinstance(list_item[key], list):
                                for list_value in list_item[key]:
                                    file.write(f"{list_value}")
                                    file.write('\n')
                            else:
                                file.write(f"{list_item[key]}")
                                file.write('\n')
                        file.write('\n')
                    else:
                        file.write(list_item)
        
        elif file_extension == '.csv':
            pass

        else:
            print('Please specify the file format')
