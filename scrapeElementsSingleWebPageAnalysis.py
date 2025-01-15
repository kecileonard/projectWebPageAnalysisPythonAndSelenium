from bs4 import BeautifulSoup
import requests
import re
from curl_cffi import requests
from urllib.parse import urljoin
from random import random
from time import sleep
import json
from pprint import pprint

class Scraper(object):

    def __init__(self, url, filepath, search_parameter=None):
        """
        Constructor for the Scraper0 class.
        """
        self.url = url
        self.filepath = filepath
        self.search_parameter = search_parameter

    def base_url(self):
        url = 'https://www.scrapingcourse.com/ecommerce/'
        return url


    def get_url(self, search_parameter=None):
        if search_parameter is not None:
            url_template = 'https://www.scrapingcourse.com/ecommerce/?orderby={}'
            url = url_template.format(search_parameter)
        else:
            url = self.base_url()
        return url


    def collect_data_from_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup


    '''function used to print the HTML Web page'''
    def show_html_content(self, url):
        html = self.process_url_request(url)
        soup = BeautifulSoup(html, 'html.parser')
        pprint(soup)


    def sleep_for_random_interval(self):
        seconds = random() * 2
        sleep(seconds)


    def extract_interactive_elements(self, soup):

        try:
            buttons = soup.find_all('button')
        except AttributeError:
            buttons = ''
            print('Could not find buttons tag. The structure of the web page might have changed.')

        try:
            # links = soup.find_all('a', attrs={'href': re.compile("^https://")})
            links = soup.find_all('a')
        except AttributeError:
            links = ''
            print('Could not find links tag  inside the structure of the web page ')

        try:
            inputs = soup.find_all('input')
        except AttributeError:
            inputs = ''
            print('Could not find input fields inside the structure of the web page')

        try:
            """Returns all form tags found on the web page of the 'url' """
            forms = soup.find_all('form')
        except AttributeError:
            forms = ''
            print('Could not find form fields inside the structure of the web page')

        try:
            navs = soup.find_all('nav')
        except AttributeError:
            navs = ''
            print('Could not find nav elements inside the structure of the web page')

        try:
            dropdowns = soup.find_all('select')
        except AttributeError:
            dropdowns = ''
            print('Could not find dropdown  inside the structure of the web page')


        # return button_tags, link_tags, input_tags, dropdowns , form_tags, select_tags ,nav_tags
        output = {
            'buttons': buttons,
            'links': links,
            'forms': forms,
            'inputs': inputs,
            'dropdowns': dropdowns,
            'navs': navs
        }
        return output


    def process_url_request(self, url):
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


    def process_links(self, links):
        data_links = []
        if links:
            # loop through the listings links to extract link attributes ,
            for link in links:
                data = {
                        'text': link.text.replace('\t', '').replace('\n', '').strip(),
                }
                if link.has_attr('href'):
                   # find the href attribute in each link
                   attr_href = link.get('href')
                   # concatenate the extracted links with the base URL to form a complete URL or use urljoin
                   if not attr_href.startswith("https"):
                       # attr_href = base_url() + attr_href
                       attr_href = urljoin(self.base_url(), link.get('href'))
                   else:
                        attr_href = link.get('href')
                        data = {
                            'href': attr_href,
                            'text': link.text.replace('\t', '').replace('\n', '').strip(),
                        }

                """ the data['class'] type is a list of values """
                if link.has_attr('class'):
                    data['class'] = link.get('class')

                if link.has_attr('aria-label'):
                    data['aria-label'] = link.get('aria-label')

                if link.has_attr('title'):
                    data['title'] = link.get('title')

                if link.has_attr('id'):
                    data['id'] = link.get('id')

                data_links.append(data)

        return data_links


    def process_forms(self, forms):
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
                    dictionary_form['inputs'] = inputs

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

        return dict_output_forms


    def process_buttons(self, buttons):
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

        return data_buttons


    def process_dropdowns(self, dropdowns):
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

        return data_dropdowns


    def process_navs(self, navs):
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

                        data = {
                            'text': list_item.text.replace('\n', '').strip(),
                        }

                        if list_item.has_attr('class'):
                            data['class'] = list_item.get('class')

                        if list_item.has_attr('id'):
                            data['id'] = list_item.get('id')

                        # Find 'a' tags with an 'href' attribute
                        attr_href = ''
                        if list_item.find('a', attrs={'href': True}):
                            attr_href = list_item.find('a').get('href')
                            if not attr_href.startswith("https"):
                                attr_href = urljoin(self.base_url(), list_item.a.get('href'))
                            data['href'] = attr_href

                        data_list_items.append(data)
                    data_navs['list_items'] = data_list_items
                dict_output_navs['nav' + str(index)] = data_navs

        return dict_output_navs


    def process_inputs(self, inputs):
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

        return data_inputs


    def save_record_to_json(self, record, filepath, create_new_file=False):
        """Save an individual record to json file; set 'new_file' flag to 'True' to generate new file"""
        json_object = json.dumps(record, indent=4, ensure_ascii=False)
        if create_new_file:
            with open(filepath, mode='w', newline='', encoding='utf-8') as file:
                pass
        else:
            with open(filepath, mode='a+', newline='', encoding='utf-8') as file:
                file.write(json_object)


    def collect_interactive_elements_attributes_from_current_page(self, output_info):
        """links data is a list of items where each item is on itself a  dictionary"""
        links_data = self.process_links(output_info['links'])

        ''' forms_data is a dict of dicts '''
        forms_data = self.process_forms(output_info['forms'])

        ''' buttons_data is a list of dicts '''
        buttons_data = self.process_buttons(output_info['buttons'])

        ''' dropdowns_data is a list of dicts '''
        dropdowns_data = self.process_dropdowns(output_info['dropdowns'])

        ''' inputs_data is a list of dicts '''
        inputs_data = self.process_inputs(output_info['inputs'])

        '''navs_data is a dict of dicts '''
        navs_data = self.process_navs(output_info['navs'])

        interactive_elements = {
            'links': links_data,
            'forms': forms_data,
            'buttons': buttons_data,
            'dropdowns': dropdowns_data,
            'inputs': inputs_data,
            'navs': navs_data,
        }
        return interactive_elements


    def main(self):
        """ record list with interactive  element attributes to save in a json file """
        record = []
        print("Start analyzing Interactive elements attributes from web page '{}'".format(self.get_url(self.search_parameter)))
        url = self.get_url(self.search_parameter)

        '''Show the HTML Web page '''
        # self.show_html_content(url)

        """ Create a new file to save json data """
        self.save_record_to_json(None, self.filepath, create_new_file=True)
        html = self.process_url_request(url)
        if not html:
            print("error")
        soup = self.collect_data_from_page(html)
        dict_interactive_elements = self.extract_interactive_elements(soup)

        """ Print Nr Interactive elements present on each page of the ecommerce  website """
        nr_links = "Nr links: '{}' ".format(len(dict_interactive_elements['links']))
        print(nr_links)

        nr_forms = "Nr Forms  : '{}' ".format(len(dict_interactive_elements['forms']))
        print(nr_forms)

        nr_buttons = "Nr Buttons: '{}' ".format(len(dict_interactive_elements['buttons']))
        print(nr_buttons)

        nr_dropdowns = "Nr DropDowns: '{}' ".format(len(dict_interactive_elements['dropdowns']))
        print(nr_dropdowns)

        nr_inputs = "Nr Inputs : '{}' ".format(len(dict_interactive_elements['inputs']))
        print(nr_inputs)

        nr_navbars = "Nr Nav's  : '{}' ".format(len(dict_interactive_elements['navs']))
        print(nr_navbars)

        """extract the interactive elements attributes for page"""
        interactive_elements = self.collect_interactive_elements_attributes_from_current_page(dict_interactive_elements)

        elements_data = {
            'Links': interactive_elements['links'],
            'Forms': interactive_elements['forms'],
            'Buttons': interactive_elements['buttons'],
            'Dropdowns': interactive_elements['dropdowns'],
            'Inputs': interactive_elements['inputs'],
            'Navs': interactive_elements['navs'],
        }

        """ record is list of dictionaries with interactive element attributes data to save in a json file """
        record.append({url: elements_data})
        """ convert record list to Json  and  save each element attributes to a json file """
        self.save_record_to_json(record, self.filepath)
        self.sleep_for_random_interval()


if __name__ == '__main__':
    url = 'https://www.scrapingcourse.com/ecommerce/'
    parameter = 'popularity'
    filepath = 'json_file.json'
    scraperObject = Scraper(url, filepath, parameter)
    scraperObject.main()