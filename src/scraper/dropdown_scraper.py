from src.scraper.scraper import Scraper
from src.common import utils


class DropdownScraper(Scraper):
    def __init__(self, url, page_url=None, search_parameter=None):
        Scraper.__init__(self, url, page_url, search_parameter)
        self.attributes = self.get_dropdowns_attributes()

    def get_all_dropdowns(self):
        try:
            soup = super().parse_page()
            list_dropdowns = soup.find_all('select')
        except AttributeError:
            list_dropdowns = ''
        return list_dropdowns

    def get_dropdowns_attributes(self) -> dict:
        dropdowns_attributes = {}
        dropdowns = self.get_all_dropdowns()
        if dropdowns is not None and len(dropdowns) > 0:
            for index, select in enumerate(dropdowns, start=1):
                dropdowns_attributes['dropdown' + str(index)] = self.get_single_dropdown_attributes(select)
        return dropdowns_attributes

    def get_single_dropdown_attributes(self, select) -> dict:
        dropdown_attributes = {}
        if select:
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

            dropdown_attributes = {
                'select_name': select_name,
                'select_class': select_class,
                'select_id': select_id,
                'select_aria_label': select_aria_label,
                'option_values': option_values,
                'option_texts': option_texts,
                'selected_value': selected_value,
                'selected_text': selected_text
            }

        return dropdown_attributes

    def get_dropdowns_data(self):
        dropdowns = self.get_all_dropdowns()
        if len(dropdowns) == 0:
            return {}
        else:
            dropdowns_data = {
                'url': self.get_url(),
                'nr_tot_dropdowns': len(self.get_all_dropdowns()),
                'dropdowns_attributes': self.attributes,
            }
        return dropdowns_data

    def __str__(self):
        return " Url: {} \n Tot Nr Dropdowns: {} \n Dropdowns Attributes: \n {}".format(self.url, len(self.get_all_dropdowns()),
                                                                                        utils.print_attributes(self.attributes))

