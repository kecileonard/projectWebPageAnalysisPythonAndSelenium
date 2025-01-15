from src.scraper.scraper import Scraper
from src.common import utils


class FormScraper(Scraper):
    def __init__(self, url, page_url=None, search_parameter=None):
        Scraper.__init__(self, url, page_url, search_parameter)
        self.attributes = self.get_forms_attributes()

    def get_all_forms(self):
        try:
            soup = super().parse_page()
            list_forms = soup.find_all('form')
        except AttributeError:
            list_forms = ''
        return list_forms

    def get_forms_attributes(self) -> dict:
        forms_attributes = {}
        forms = self.get_all_forms()
        if forms:
            for index, form in enumerate(forms, start=1):
                forms_attributes['form' + str(index)] = self.get_single_form_attributes(form)
        return forms_attributes

    def get_single_form_attributes(self, form) -> dict:
        form_attributes = {}
        if form:
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
            form_attributes['form_attrs'] = form_attrs_data

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
                form_attributes['inputs'] = inputs

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
                form_attributes['select_options'] = options
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
                form_attributes['textareas'] = textareas

        return form_attributes

    def get_forms_data(self):

        forms = self.get_all_forms()
        if len(forms) == 0:
            return {}
        else:
            forms_data = {
                'url': self.get_url(),
                'nr_tot_forms': len(self.get_all_forms()),
                'forms_attributes': self.attributes,
            }
        return forms_data

    def __str__(self):
        return " Url: {} \n Tot Nr Forms: {} \n Forms Attributes: \n {}".format(self.url, len(self.get_all_forms()),
                                                                                utils.print_attributes(
                                                                                      self.attributes))

