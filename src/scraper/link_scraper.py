from src.scraper.scraper import Scraper
from src.common import utils
from urllib.parse import urljoin


class LinkScraper(Scraper):
    def __init__(self, url, page_url=None, search_parameter=None):
        Scraper.__init__(self, url, page_url, search_parameter)
        self.attributes = self.get_links_attributes()


    def get_all_links(self):
        try:
            soup = super().parse_page()
            #list_links  = soup.find_all('a', attrs={'href': re.compile("^https://")})
            list_links = soup.find_all('a')
        except AttributeError:
            list_links = ''

        return list_links


    def get_links_attributes(self) -> dict:
        links_attributes = {}
        links = self.get_all_links()
        if links:
            for index, link in enumerate(links, start=1):
                links_attributes['link' + str(index)] = self.get_single_link_attributes(link)
        return links_attributes

    def get_single_link_attributes(self, link) -> dict:
        link_attributes = {}
        if link:
            link_attributes = {
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
                    link_attributes = {
                        'href': attr_href,
                        'text': link.text.replace('\t', '').replace('\n', '').strip(),
                    }

            """ the data['class'] type is a list of values """
            if link.has_attr('class'):
                link_attributes['class'] = link.get('class')

            if link.has_attr('aria-label'):
                link_attributes['aria-label'] = link.get('aria-label')

            if link.has_attr('title'):
                link_attributes['title'] = link.get('title')

            if link.has_attr('id'):
                link_attributes['id'] = link.get('id')

        return link_attributes

    def get_links_data(self):
        """
        Get all the links data presented in this page.
        Return a dictionary of link attributes
        """
        links = self.get_all_links()
        if len(links) == 0:
            return {}
        else:
            links_data = {
                'url': self.get_url(),
                'nr_tot_links': len(self.get_all_links()),
                'links_attributes': self.attributes,
            }
        return links_data


    def __str__(self):
        return " Url: {} \n Tot Nr Links: {} \n Links Attributes: \n {}".format(self.url, len(self.get_all_links()),
                                                                                utils.print_attributes(self.attributes))




