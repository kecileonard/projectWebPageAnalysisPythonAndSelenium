from src.scraper.button_scraper import ButtonScraper
from src.scraper.link_scraper import LinkScraper
from src.scraper.dropdown_scraper import DropdownScraper
from src.scraper.nav_scraper import NavScraper
from src.scraper.input_scraper import InputScraper
from src.scraper.form_scraper import FormScraper
from src.common import utils


def main():
    url = 'https://www.scrapingcourse.com/ecommerce'
    search_parameter = 'popularity'
    path_file_json = 'src/export_files/recordDataPage_'
    path_file_txt = 'src/export_files/analysisDataPage.txt'
    path_file_csv = '#'
    pathFile = [path_file_json, path_file_txt, path_file_csv]
    list_count = []

    utils.save_record_to_files(None, pathFile[1], create_new_file=True)
    for page_url in range(1, 7):  # take the first 6 /The max nr pages showed in the content webpage  is 12.
        recordData = []
        page = "Start Analyzing and scraping interactive elements attributes for the {} page ".format(page_url)
        print(page)
        utils.save_record_to_files(None, pathFile[0] + str(page_url) + ".json", create_new_file=True)

        buttonScraperObj = ButtonScraper(url, page_url, search_parameter)
        linkScraperObj = LinkScraper(url, page_url, search_parameter)
        dropdownScraperObj = DropdownScraper(url, page_url, search_parameter)
        navScraperObj = NavScraper(url, page_url, search_parameter)
        inputScraperObj = InputScraper(url, page_url, search_parameter)
        formScraperObj = FormScraper(url, page_url, search_parameter)
        '''
        print(buttonScraperObj)
        print(dropdownScraperObj)
        print(navScraperObj)
        print(inputScraperObj)
        print(formScraperObj)
        print(linkScraperObj)
        print(linkScraperObj)
        '''
        """Json data of each  Interactive elements """
        recordData.append(linkScraperObj.get_links_data())
        recordData.append(formScraperObj.get_forms_data())
        recordData.append(buttonScraperObj.get_buttons_data())
        recordData.append(dropdownScraperObj.get_dropdowns_data())
        recordData.append(inputScraperObj.get_inputs_data())
        recordData.append(navScraperObj.get_navs_data())

        """  Nr Interactive elements present on each page of the  website """
        links_data = linkScraperObj.get_links_data()
        forms_data = formScraperObj.get_forms_data()
        buttons_data = buttonScraperObj.get_buttons_data()
        dropdowns_data = dropdownScraperObj.get_dropdowns_data()
        inputs_data = inputScraperObj.get_inputs_data()
        navs_data = navScraperObj.get_navs_data()

        url_page = links_data.get('url')
        nr_links = "Nr links: {}".format(links_data.get('nr_tot_links'))
        nr_forms = "Nr Forms: {}".format(forms_data.get('nr_tot_forms'))
        nr_buttons = "Nr Buttons: {}".format(buttons_data.get('nr_tot_buttons'))
        nr_dropdowns = "Nr DropDowns: {}".format(dropdowns_data.get('nr_tot_dropdowns'))
        nr_inputs = "Nr Inputs: {}".format(inputs_data.get('nr_tot_inputs'))
        nr_navbars = "Nr Nav's: {}".format(navs_data.get('nr_tot_navs'))

        element_count = [
            nr_links,
            nr_forms,
            nr_buttons,
            nr_dropdowns,
            nr_inputs,
            nr_navbars,
        ]

        dictionary_element_count = {url_page: element_count}
        list_count.append(dictionary_element_count)

        utils.sleep_time()
        utils.save_record_to_files(recordData, pathFile[0] + str(page_url) + ".json")
    utils.save_record_to_files(list_count, pathFile[1])

    print("Analysis completed !")


if __name__ == '__main__':
    main()


