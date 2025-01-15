from src.scraper.scraper import Scraper
from src.common import utils


class ButtonScraper(Scraper):
    def __init__(self, url, page_url=None, search_parameter=None):
        Scraper.__init__(self, url, page_url, search_parameter)
        self.attributes = self.get_buttons_attributes()

    def get_all_buttons(self):
        try:
            soup = super().parse_page()
            list_buttons = soup.find_all('button')
        except AttributeError:
            list_buttons = ''

        return list_buttons

    def get_buttons_attributes(self) -> dict:
        buttons_attributes = {}
        buttons = self.get_all_buttons()
        if buttons:
            for index, button in enumerate(buttons, start=1):
                buttons_attributes['button' + str(index)] = self.get_single_button_attributes(button)
        return buttons_attributes

    def get_single_button_attributes(self, button) -> dict:
        button_attributes = {}
        if button:
            button_attributes = {
                'text': button.text.replace('\t', '').replace('\n', '').strip(),
                'id': button.get('id'),
                'type': button.get('type'),
            }

            if button.has_attr('aria-label'):
                button_attributes['aria-label'] = button.get('aria-label')

            if button.has_attr('class'):
                button_attributes['class'] = button.get('class')

            if button.has_attr('data-testid'):
                button_attributes['data-testid'] = button.get('data-testid')

            if button.has_attr('data-nav'):
                button_attributes['data-nav'] = button.get('data-nav')

            if button.has_attr('value'):
                button_attributes['value'] = button.get('value')

        return button_attributes

    def get_buttons_data(self):
        """
        Get all the buttons data presented in this page.
        Return a dictionary
        :return: dict button data
        """
        buttons = self.get_all_buttons()
        if len(buttons) == 0:
            return {}
        else:
            buttons_data = {
                'url': self.get_url(),
                'nr_tot_buttons': len(self.get_all_buttons()),
                'buttons_attributes': self.attributes,
            }
        return buttons_data


    def __str__(self):
        return " Url: {} \n Tot Nr Buttons: {} \n Buttons Attributes: \n {}".format(self.get_url(), len(self.get_all_buttons()),
                                                                                    utils.print_attributes(self.attributes))


