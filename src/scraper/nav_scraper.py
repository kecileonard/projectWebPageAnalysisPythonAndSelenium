from src.scraper.scraper import Scraper
from src.common import utils
from urllib.parse import urljoin


class NavScraper(Scraper):
    def __init__(self, url, page_url=None, search_parameter=None):
        Scraper.__init__(self, url, page_url, search_parameter)
        self.attributes = self.get_navs_attributes()

    def get_all_navs(self):
        try:
            html = super().process_url_request()
            if not html:
                print("error")
            soup = super().parse_page()
            list_navs = soup.find_all('nav')
        except AttributeError:
            list_navs = ''

        return list_navs

    def get_navs_attributes(self) -> dict:
        navs_attributes = {}
        navs = self.get_all_navs()
        if navs:
            for index, nav in enumerate(navs, start=1):
                navs_attributes['nav' + str(index)] = self.get_single_nav_attributes(nav)
        return navs_attributes

    def get_single_nav_attributes(self, nav) -> dict:
        nav_attributes = {}
        if nav:
            data = {
                'id': nav.get('id'),
                'class': nav.get('class'),
                'data-testid': nav.get('data-testid'),
            }
            if nav.has_attr('aria-label'):
                data['aria-label'] = nav.get('aria-label')

            if nav.has_attr('role'):
                data['role'] = nav.get('role')

            nav_attributes['nav_attrs'] = data

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
                nav_attributes['nav_list_items'] = data_list_items

        return nav_attributes

    def get_navs_data(self):
        """
        Get all the navs data presented in this page.
        Return a dictionary of navs attributes
        """
        navs = self.get_all_navs()
        if len(navs) == 0:
            return {}
        else:
            navs_data = {
                'url': self.get_url(),
                'nr_tot_navs': len(self.get_all_navs()),
                'navs_attributes': self.attributes,
            }
        return navs_data

    def __str__(self):
        return " Url: {} \n Tot Nr Navs: {} \n Navs Attributes: \n {}".format(self.url, len(self.get_all_navs()),
                                                                              utils.print_attributes(self.attributes))



