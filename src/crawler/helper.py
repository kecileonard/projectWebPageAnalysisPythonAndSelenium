from bs4 import BeautifulSoup
import requests
from curl_cffi import requests
from urllib.parse import urljoin
import re

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
    try:
        buttons = soup.find_all('button')
    except AttributeError:
        print('Could not find buttons tag. The structure of the web page might have changed.')
        buttons = ''
    try:
        # links = soup.find_all('a', attrs={'href': re.compile("^https://")})
        links = soup.find_all('a')
    except AttributeError:
        print('Could not find links tag  inside the structure of the web page ')
        links = ''
    # return button_tags, link_tags, input_tags, dropdowns , form_tags, select_tags
    output = {
        'buttons': buttons,
        'links': links,
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

            data = {
                # 'href': attr_href,
                'text': link.text.replace('\t', '').replace('\n', '').strip(),
            }
            if link.has_attr('href'):
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

    return data_buttons

def collect_interactive_elements_attributes_from_current_page(output_info):
    ''' links data is a list of items where each item is on itself a  dictionary '''
    links_data = process_links(output_info['links'])
    ''' buttons_data is a list of dicts '''
    buttons_data = process_buttons(output_info['buttons'])

    interactive_elements = {
        'links': links_data,
        'buttons': buttons_data,
    }
    return interactive_elements
