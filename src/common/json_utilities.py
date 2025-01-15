import json


def convert_list_to_json(list):
    """
    Converts a list to a JSON object
    :param list: list to convert
    :return: JSON object
    """
    try:
        json_obj = json.dumps(list)
        return json_obj
    except Exception as e:
        print(e)

def convert_string_to_json(string: str):
    """
    Converts a string to a JSON object
    :param string: string to convert
    :return: JSON object
    """
    try:
        return json.loads(string)
    except Exception as e:
        print(e)
