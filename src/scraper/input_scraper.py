from src.scraper.scraper import Scraper
from src.common import utils


class InputScraper(Scraper):
    def __init__(self, url, page_url=None, search_parameter=None):
        Scraper.__init__(self, url, page_url, search_parameter)
        self.attributes = self.get_inputs_attributes()

    def get_all_inputs(self):
        try:
            soup = super().parse_page()
            list_inputs = soup.find_all('input')
        except AttributeError:
            list_inputs = ''
        return list_inputs

    def get_inputs_attributes(self) -> dict:
        inputs_attributes = {}
        inputs = self.get_all_inputs()
        if inputs:
            for index, input in enumerate(inputs, start=1):
                inputs_attributes['input' + str(index)] = self.get_single_input_attributes(input)
        return inputs_attributes

    def get_single_input_attributes(self, input) -> dict:
        input_attributes = {}
        if input:
            input_attributes = {
                'type': input.get('type'),
                'id': input.get('id'),
                'value': input.get('value'),
                'name': input.get('name'),
                'data-testid': input.get('data-testid')
            }

            if input.has_attr('class'):
                input_attributes['class'] = input.get('class')

            if input.has_attr('placeholder'):
                input_attributes['placeholder'] = input.get('placeholder')
        return input_attributes

    def get_inputs_data(self):
        """
        Get all the inputs data presented in this page.
        Return a dictionary
        :return: dict input data
        """
        inputs = self.get_all_inputs()
        if len(inputs) == 0:
            return {}
        else:
            inputs_data = {
                'url': self.get_url(),
                'nr_tot_inputs': len(self.get_all_inputs()),
                'buttons_attributes': self.attributes,
            }
        return inputs_data


    def __str__(self):
        return " Url: {} \n Tot Nr Inputs: {} \n Inputs Attributes: \n {}".format(self.url, len(self.get_all_inputs()),
                                                                                  utils.print_attributes(self.attributes))

