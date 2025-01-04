from bs4 import BeautifulSoup
import requests
import re
from curl_cffi import requests
from urllib.parse import urljoin
from random import random
from time import sleep
import json
from pprint import pprint
import os

""" Selenium libs"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def base_url():
    url = 'https://www.scrapingcourse.com/ecommerce/'
    return url


def get_url(search_parameter=None):
    if search_parameter is not None:
        url_template = f'https://www.scrapingcourse.com/ecommerce/?orderby={search_parameter}'
        url = url_template.format(search_parameter)
    else:
        url = base_url()
    return url


def collect_data_from_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup


'''function used to print the HTML Web page'''
def show_html_content(url):
    html = process_url_request(url)
    soup = BeautifulSoup(html, 'html.parser')
    pprint(soup)


def sleep_for_random_interval():
    seconds = random() * 2
    sleep(seconds)


def find_next_page(page, parameter=None):
    if parameter is not None:
        if page == 1:
            url = get_url(parameter)
        else:
            base_template = f'https://www.scrapingcourse.com/ecommerce/page/{page}/?orderby={parameter}'
            steam = base_template.format(parameter)
            url = steam.format(page)
        return url
    else:
        if page == 1:
            url = get_url(parameter)
        else:
            base_template = f'https://www.scrapingcourse.com/ecommerce/page/{page}'
            steam = base_template.format(parameter)
            url = steam.format(page)
    return url


def extract_interactive_elements(soup):
    inputs = []
    links = []
    buttons = []
    forms = []
    dropdowns = []
    navs = []

    try:
        buttons = soup.find_all('button')
    except AttributeError:
        print('Could not find buttons tag. The structure of the web page might have changed.')

    try:
        # links = soup.find_all('a', attrs={'href': re.compile("^https://")})
        links = soup.find_all('a')
    except AttributeError:
        print('Could not find links tag  inside the structure of the web page ')

    try:
        inputs = soup.find_all('input')
    except AttributeError:
        print('Could not find input fields inside the structure of the web page')

    try:
        """Returns all form tags found on the web page of the 'url' """
        forms = soup.find_all('form')
    except AttributeError:
        print('Could not find form fields inside the structure of the web page')

    try:
        navs = soup.find_all('nav')
    except AttributeError:
        print('Could not find nav elements inside the structure of the web page')

    try:
        dropdowns = soup.find_all('select')
    except AttributeError:
        print('Could not find dropdown  inside the structure of the web page')

    # return button_tags, link_tags, input_tags, dropdowns , form_tags, select_tags
    output = {
        'buttons': buttons,
        'links': links,
        'forms': forms,
        'inputs': inputs,
        'dropdowns': dropdowns,
        'navs': navs

    }
    return output


def process_url_request(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    if response.status_code == 200:
        return response.text
    else:
        return None


def process_links(links):
    data_links = []
    if links:
        # loop through the listings links to extract link attributes ,
        for link in links:
            # find the href attribute in each link
            attr_href = link.get('href')
            # concatenate the extracted links with the base URL to form a complete URL or use urljoin
            if not attr_href.startswith("https"):
                # attr_href = base_url() + attr_href
                attr_href = urljoin(base_url(), link.get('href'))
            else:
                attr_href = link.get('href')

            data = {
                'href': attr_href,
                'text': link.text.replace('\t', '').replace('\n', '').strip(),

            }
            ''' the data['class'] type is a list of values '''
            if link.has_attr('class'):
                data['class'] = link.get('class')
            '''
            in case the data['class'] needs to be represented as a tuple of values 
            if link.has_attr('class'):                
                list = []
                for cl in link.get('class'):
                    #Adding num to list
                    list.append(cl)                
                my_tuple =tuple(my_list)
                data['class'] = my_tuple
            '''
            if link.has_attr('aria-label'):
                data['aria-label'] = link.get('aria-label')

            if link.has_attr('title'):
                data['title'] = link.get('title')

            if link.has_attr('id'):
                data['id'] = link.get('id')

            data_links.append(data)
    else:
        print('Links  not found in the page')
        ''' data_links is a list of items where each item is on itself a list of dictionaries '''
    return data_links


def process_forms(forms):
    dict_output_forms = {}

    if forms:
        # loop through the forms to extract each form tag attributes ,
        for index, form in enumerate(forms, start=1):
            form_attrs_data = []
            dictionary_form = {}
            data = {
                'role': form.get('role'),
                'method': form.get('method'),
                'action': form.get('action'),
                'class': form.get('class'),
                'id': form.get(id),
                'text': form.text.replace('\n', '').strip(),
            }
            form_attrs_data.append(data)
            dictionary_form['form_attrs'] = form_attrs_data

            input_tags = form.find_all("input")
            if input_tags is not None and len(input_tags) > 0:
                inputs = []
                for input_tag in input_tags:
                    # get type of input form control
                    input_type = input_tag.attrs.get("type", "text")
                    # get name attribute
                    input_name = input_tag.attrs.get("name")
                    # get id attribute
                    input_id = input_tag.attrs.get("id")
                    # get the default value of that input tag
                    input_value = input_tag.attrs.get("value", "")

                    data = {
                        'type': input_type,
                        'name': input_name,
                        'value': input_value,
                        'id': input_id,
                    }
                    inputs.append(data)
                dictionary_form['form_inputs'] = inputs

            select_tags = form.find_all("select")
            if select_tags is not None and len(select_tags) > 0:
                options = []
                for select in select_tags:
                    # get the select tag  attributes
                    select_name = select.attrs.get("name")
                    select_class = select.attrs.get("class")
                    select_id = select.attrs.get("id")
                    select_aria_label = select.attrs.get("aria-label")
                    option_values = []
                    option_texts = []
                    # the selected value
                    selected_value = ""
                    selected_text = ""
                    # iterate over options and get the value of each
                    for select_option in select.find_all("option"):
                        # get the option value used to submit the form
                        option_value = select_option.attrs.get("value")
                        if option_value:
                            option_text = select_option.text
                            option_values.append(option_value)
                            option_texts.append(option_text)
                            if select_option.attrs.get("selected"):
                                # if 'selected' attribute is set, set this option as default
                                selected_value = option_value
                                selected_text = select_option.text

                    if not selected_value and option_values:
                        # if the default is not set, and there are options, take the first option as default
                        selected_value = option_values[0]

                    data = {
                        'select_name': select_name,
                        'select_class': select_class,
                        'select_id': select_id,
                        'select_aria_label': select_aria_label,
                        'option_values': option_values,
                        'option_texts': option_texts,
                        'selected_value': selected_value,
                        'selected_text': selected_text
                    }
                    options.append(data)
                dictionary_form['select_options'] = options
            # for textarea input fields
            textarea = form.find_all("textarea")
            if textarea is not None and len(textarea) > 0:
                textareas = []
                for textarea in form.find_all("textarea"):
                    # get the name attribute
                    textarea_name = textarea.attrs.get("name")
                    # set the type as textarea
                    textarea_type = "textarea"
                    # get the textarea value
                    textarea_value = textarea.attrs.get("value", "")
                    # add the textarea to the inputs list
                    data = {
                        'type': textarea_type,
                        'name': textarea_name,
                        'value': textarea_value
                    }
                    textareas.append(data)
                dictionary_form['textareas'] = textareas

            dict_output_forms['form' + str(index)] = dictionary_form

    else:
        print('Forms not found in the web page')

    return dict_output_forms


def process_buttons(buttons):
    data_buttons = []
    if buttons:
        for button in buttons:
            data = {
                'text': button.text.replace('\t', '').replace('\n', '').strip(),
                'id': button.get('id'),
                'type': button.get('type'),
            }

            if button.has_attr('aria-label'):
                data['aria-label'] = button.get('aria-label')

            if button.has_attr('class'):
                data['class'] = button.get('class')

            if button.has_attr('data-testid'):
                data['data-testid'] = button.get('data-testid')

            if button.has_attr('data-nav'):
                data['data-nav'] = button.get('data-nav')

            if button.has_attr('value'):
                data['value'] = button.get('value')

            data_buttons.append(data)
    else:
        print('Buttons tags not found in the page')
    return data_buttons


def process_dropdowns(dropdowns):
    data_dropdowns = []
    if dropdowns is not None and len(dropdowns) > 0:
        for select in dropdowns:
            # get the select tag  attributes
            select_name = select.attrs.get("name")
            select_class = select.attrs.get("class")
            select_id = select.attrs.get("id")
            select_aria_label = select.attrs.get("aria-label")
            option_values = []
            option_texts = []
            selected_value = ""
            selected_text = ""
            # iterate over options and get the each option value
            for select_option in select.find_all("option"):
                # get the option value used to submit the form
                option_value = select_option.attrs.get("value")
                if option_value:
                    option_text = select_option.text
                    option_values.append(option_value)
                    option_texts.append(option_text)
                    if select_option.attrs.get("selected"):
                        # if 'selected' attribute is set, set this option as default
                        selected_value = option_value
                        selected_text = select_option.text

            if not selected_value and option_values:
                # if the default is not set, and there are options, take the first option as  default
                selected_value = option_values[0]

            data = {
                'select_name': select_name,
                'select_class': select_class,
                'select_id': select_id,
                'select_aria_label': select_aria_label,
                'option_values': option_values,
                'option_texts': option_texts,
                'selected_value': selected_value,
                'selected_text': selected_text
            }
            data_dropdowns.append(data)
    else:
        print('Select tags  not found in the web page')
    return data_dropdowns


def process_navs(navs):
    dict_output_navs = {}

    if navs is not None and len(navs) > 0:
        for index, nav in enumerate(navs, start=1):

            data_navs = {}
            data = {
                'id': nav.get('id'),
                'class': nav.get('class'),
                'data-testid': nav.get('data-testid'),
            }
            if nav.has_attr('aria-label'):
                data['aria-label'] = nav.get('aria-label')

            if nav.has_attr('role'):
                data['role'] = nav.get('role')

            data_navs['nav_attrs'] = data

            list_items = nav.find_all('li')
            if list_items:
                # loop through the listings items to extract link attributes ,
                data_list_items = []
                for list_item in list_items:

                    data_li = {
                        'text': list_item.text.replace('\n', '').strip(),
                    }

                    if list_item.has_attr('class'):
                        data_li['class'] = list_item.get('class')

                    if list_item.has_attr('id'):
                        data_li['id'] = list_item.get('id')

                    # Find 'a' tags with an 'href' attribute
                    attr_href = ''
                    if list_item.find('a', attrs={'href': True}):
                        attr_href = list_item.find('a').get('href')
                        if not attr_href.startswith("https"):
                            attr_href = urljoin(base_url(), list_item.a.get('href'))
                        data_li['href'] = attr_href

                    data_list_items.append(data_li)
                data_navs['list_items'] = data_list_items
            dict_output_navs['nav' + str(index)] = data_navs

    else:
        print('Navs  not found in the web page')

    return dict_output_navs


def process_inputs(inputs):
    data_inputs = []
    if inputs:
        for input in inputs:

            data = {
                'type': input.get('type'),
                'id': input.get('id'),
                'value': input.get('value'),
                'name': input.get('name'),
                'data-testid': input.get('data-testid')
            }

            if input.has_attr('class'):
                data['class'] = input.get('class')

            if input.has_attr('placeholder'):
                data['placeholder'] = input.get('placeholder')

            data_inputs.append(data)
    else:
        print('Input fields  not found in the page')
    return data_inputs


def save_record_to_files(record, pathFile, create_new_file=False):
    if create_new_file:

        with open(pathFile[0], mode='w', newline='', encoding='utf-8') as file_js:
            pass

        with open(pathFile[1], mode='w', newline='', encoding='utf-8') as file_txt:
            pass

    else:
        split_tup = os.path.splitext(pathFile)
        file_name = split_tup[0]
        file_extension = split_tup[1]

        if file_extension == '.json':
            """Save an individual record to json file; set 'create_new_file' flag to 'True' to generate new file and save"""
            json_object = json.dumps(record, indent=4, ensure_ascii=False)
            with open(pathFile, mode='a+', newline='', encoding='utf-8') as file_js:
                file_js.write(json_object)


        elif file_extension == '.txt':
            with open(pathFile, mode='a+', newline='', encoding='utf-8') as file_txt:
                for i, list_item in enumerate(record):
                    if isinstance(list_item, dict):
                        for j, key in enumerate(list_item.keys()):
                            file_txt.write(f"{key}")
                            file_txt.write('\n')
                            if isinstance(list_item[key], list):
                                for list_value in list_item[key]:
                                    file_txt.write(f"{list_value}")
                                    file_txt.write('\n')
                            else:
                                file_txt.write(f"{list_item[key]}")
                                file_txt.write('\n')
                        file_txt.write('\n')
                    else:
                        file_txt.write(list_item)

        elif file_extension == '.csv':
            pass
        else:
            print('Please specify the file format')


def main(pathFile, search_parameter=None):
    counter = 0
    record = []
    list_count = []

    """ Create 2 new .json and .txt files and: 
        Save each interactive element attributes such us id, name,  class , href , title ,text , value ect  in json format 
        Save the number of interactive elements present  on each analysed page
    """
    save_record_to_files(None, pathFile, create_new_file=True)

    for page in range(1, 13):  # max of 12 pages showed in the website

        # load the next page
        url = find_next_page(page, search_parameter)
        print("Analyzing and scraping interactive elements attributes  from web page '{}'".format(url))
        url_page = "Start analyzing and scraping interactive elements attributes  from web page '{}'".format(url)

        '''show_html_content function used to show the HTML Web page '''
        # show_html_content(url)

        html = process_url_request(url)
        if not html:
            break
        soup = collect_data_from_page(html)
        output_info = extract_interactive_elements(soup)

        """ Print Nr Interactive elements present on each page of the ecommerce  website """
        nr_links = "Nr links: '{}' ".format(len(output_info['links']))
        print(nr_links)

        nr_forms = "Nr Forms  : '{}' ".format(len(output_info['forms']))
        print(nr_forms)

        nr_buttons = "Nr Buttons: '{}' ".format(len(output_info['buttons']))
        print(nr_buttons)

        nr_dropdowns = "Nr DropDowns: '{}' ".format(len(output_info['dropdowns']))
        print(nr_dropdowns)

        nr_inputs = "Nr Inputs : '{}' ".format(len(output_info['inputs']))
        print(nr_inputs)

        nr_navbars = "Nr Nav's  : '{}' ".format(len(output_info['navs']))
        print(nr_navbars)

        element_count = [
            nr_links,
            nr_forms,
            nr_buttons,
            nr_dropdowns,
            nr_inputs,
            nr_navbars,
        ]

        dictionary = {url_page: element_count}
        list_count.append(dictionary)

        """ process interactive elements and extract the data attributes """
        ''' links data is a list of items where each item is on itself a list of dictionaries '''
        links_data = process_links(output_info['links'])
        ''' forms_data is a dict of dicts '''
        forms_data = process_forms(output_info['forms'])
        ''' buttons_data is a list of dicts '''
        buttons_data = process_buttons(output_info['buttons'])
        ''' dropdowns_data is a list of dicts '''
        dropdowns_data = process_dropdowns(output_info['dropdowns'])
        ''' inputs_data is a list of dicts '''
        inputs_data = process_inputs(output_info['inputs'])
        '''navs_data is a dict of dicts '''
        navs_data = process_navs(output_info['navs'])

        elements_data = {
            'Links': links_data,
            'Forms': forms_data,
            'Buttons': buttons_data,
            'Dropdowns': dropdowns_data,
            'Inputs': inputs_data,
            'Navs': navs_data,
        }

        """ record is list of dictionaries with interactive element attributes data to save in a json file """
        record.append({url: elements_data})

        sleep_for_random_interval()
        counter += 1


    """" convert record list to Json format and  save each element attributes in json file """
    save_record_to_files(record, pathFile[0])

    print('Finished collecting data of Interactive elements in {:,d} pages.'.format(counter))
    tot_pages_analysed = 'Finished collecting data of Interactive elements in {:,d} pages.'.format(counter)

    list_count.append(tot_pages_analysed)
    """" save each  element attributes count for each page in a txt file """
    save_record_to_files(list_count, pathFile[1])


if __name__ == '__main__':
    parameter = 'popularity'
    path_file_json = 'jsonFileMultiplePages.json'
    path_file_txt = 'txtFileCountElements.txt'
    path_file_csv = 'test.csv'
    pathFile = [path_file_json, path_file_txt, path_file_csv]
    # main(pathFiles)
    main(pathFile, parameter)
