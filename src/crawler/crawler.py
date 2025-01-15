from src.crawler import helper


def crawl_url(input_url, visited, urls_to_crawl):
    """
         The Crawler function visit and finds all the links from the starting web page.
         Traverse each page starting form the base link and apply the extraction logic on each page .
         It gets  new urls and then traverse each url one by one collecting  interactive elements attributes .
         It gets a new URL from the queue, adds it to the list of visited pages, sends the request, parses the web pages, and extracts data.
         The crawler process continues repeatedly  until there are no more pages from seed url.
    """
    links_page = []

    if input_url not in visited:
        visited.add(input_url)

    html = helper.process_url_request(input_url)
    if not html:
        return 'error can not parse html page '

    soup = helper.collect_data_from_page(html)
    output_data = helper.extract_interactive_elements(soup)
    interactive_elements = helper.collect_interactive_elements_attributes_from_current_page(output_data)

    for dictionary in interactive_elements['links']:
        if 'href' in dictionary.keys():
            if dictionary['href']:
                links_page.append((dictionary['href']))
        else:
            print("No href attribute !")
    #print(links_page)

    # remove external links such us https://woo.com to avoid go outside internal website
    list_links = [link for link in links_page if helper.base_url() in link]

    # remove from the links list the image links jpg suffix to not crawler
    #regex = "([^\\s]+(\\.(?i)(jpe?g|png|gif|bmp))$)"
    #regex = re.compile(regex, re.IGNORECASE)

    regex = helper.re.compile('\.jpg$|\.gif$|\.png$', helper.re.IGNORECASE)
    list_links = filter(lambda url: not regex.search(url), list_links)

    # Checking if the URL is not already visited or in the list of URLs to visit
    for link in list_links:
        if link not in urls_to_crawl and link not in visited:
            urls_to_crawl.add(link)
    return output_data


def main():
    #url = 'https://www.scrapingcourse.com/ecommerce'
    search_parameter = 'popularity'
    urls_to_crawl = set()
    visited = set()

    for page_url in range(1, 13):  # max of 12 pages showed in the website

        # load the next page
        seed_url = helper.find_next_page(page_url, search_parameter)  # seed url for the crawler

        urls_to_crawl.add(seed_url)

        while len(urls_to_crawl):  # Loop until there are still urls to visit

            url_to_crawl = urls_to_crawl.pop()  # Get the next URL to visit from the list
            print("Analyzing  web page '{}'".format(url_to_crawl))

            try:
                data_extracted = crawl_url(url_to_crawl, visited, urls_to_crawl)  # Crawl the web page
                """ Buttons and Inputs attributes will be used by Selenium to click on them """
                record_list_of_tuples = [
                    ('Nr Buttons', len(data_extracted['buttons'])),
                    ('Nr Links', len(data_extracted['links']))
                ]
                #print(record_list_of_tuples)

            except Exception as error:
                print(f'Failed to crawl: {url_to_crawl}')  # Handling exceptions
                print("An exception occurred:", error)


if __name__ == '__main__':
    main()
