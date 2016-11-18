from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait

import settings


class CompanyDataScraper():

    def __init__(self):
        self.driver = webdriver.PhantomJS()

    # Parse raw cells and related rows and append to data accounting data
    @staticmethod
    def parse_raw_accounting_data(first_cell, second_cell, data, brother, great_brother):
        if second_cell:
            # BILANT

            # active
            if 'imobilizate' in first_cell.lower():
                data['bilant']['active']['categories']['imobilizate'] = \
                    int(second_cell)
            elif 'circulante' in first_cell.lower():
                data['bilant']['active']['categories']['circulante']['total'] = \
                    int(second_cell)
            elif 'stocuri' in first_cell.lower():
                data['bilant']['active']['categories']['circulante']['categories'][
                    'stocuri'] = \
                    int(second_cell)
            elif 'creante' in first_cell.lower():
                data['bilant']['active']['categories']['circulante']['categories'][
                    'creante'] = \
                    int(second_cell)
            elif 'casa' in first_cell.lower():
                data['bilant']['active']['categories']['circulante']['categories'][
                    'casa'] = \
                    int(second_cell)

            # avans
            elif 'cheltuieli in avans' in first_cell.lower():
                data['bilant']['cheltuieli_in_avans'] = int(second_cell)
            elif 'venituri in avans' in first_cell.lower():
                data['bilant']['venituri_in_avans'] = int(second_cell)

            # datorii
            elif 'datorii' in first_cell.lower():
                data['bilant']['datorii'] = int(second_cell)

            # capitaluri
            elif 'capitaluri' in first_cell.lower():
                data['bilant']['capitaluri']['total'] = int(second_cell)
            elif 'subscris' in first_cell.lower():
                data['bilant']['capitaluri']['categories']['subscris'] = int(
                    second_cell)
            elif 'patrimoniul regiei' in first_cell.lower():
                data['bilant']['capitaluri']['categories']['patrimoniul_regiei'] = \
                    int(second_cell)
            elif 'patrimoniul public' in first_cell.lower():
                data['bilant']['capitaluri']['categories']['patrimoniul_public'] = \
                    int(second_cell)

            # CONT PROFIT SI PIERDERE

            elif 'cifra de afaceri' in first_cell.lower():
                data['cpp']['cifra_de_afaceri_neta'] = int(second_cell)
            elif 'venituri' in first_cell.lower():
                data['cpp']['venituri_totale'] = int(second_cell)
            elif 'cheltuieli' in first_cell.lower():
                data['cpp']['cheltuieli_totale'] = int(second_cell)

            # profituri
            elif 'profit' in first_cell.lower():
                if 'brut' in brother.find_elements_by_tag_name('td')[0].text:
                    data['cpp']['profit']['brut'] = int(second_cell)
                elif 'net' in brother.find_elements_by_tag_name('td')[0].text:
                    data['cpp']['profit']['net'] = int(second_cell)

            # pierderi
            elif 'pierdere' in first_cell.lower():
                if 'brut' in great_brother.find_elements_by_tag_name('td')[0].text:
                    data['cpp']['pierdere']['brut'] = int(second_cell)
                elif 'net' in great_brother.find_elements_by_tag_name('td')[0].text:
                    data['cpp']['pierdere']['net'] = int(second_cell)

            # INFORMATII SUPLIMENTARE

            elif 'salariati' in first_cell.lower():
                data['informatii']['salariati'] = int(second_cell)
            elif 'caen' in first_cell.lower():
                data['informatii']['caen'] = second_cell
        return data

    def scrape_pretty_data(self, url):
        return self.scrape_link(url=url)

    def scrape_raw_data(self, url):
        return self.scrape_link(url,
                                raw=True)

    def scrape_link(self, url, raw=False):

        # allow modifications such as User Agent
        desired_capabilities = dict(DesiredCapabilities.PHANTOMJS)
        self.driver.start_session(desired_capabilities)
        self.driver.get(url)

        # recursive defaultdict(dict)
        def recursive_dict():
            return defaultdict(recursive_dict)
        data = defaultdict(recursive_dict)
        error = ''

        try:
            # wait until element found on page
            WebDriverWait(self.driver, settings.TIMEOUT).until(
                lambda driver: driver.find_element_by_tag_name(settings.ELEMENT_TAG))
            element = self.driver.find_element_by_tag_name(settings.ELEMENT_TAG)

            # start parsing the table
            brother = None
            great_brother = None
            for row in element.find_elements_by_tag_name('tr'):
                if len(row.find_elements_by_tag_name('td')) == 2:
                    first_cell = row.find_elements_by_tag_name('td')[0].text
                    second_cell = row.find_elements_by_tag_name('td')[1].text

                    # clean - from second cell
                    if second_cell == '-':
                        second_cell = 0

                    if raw:
                        data[first_cell] = second_cell
                    else:
                        data = self.parse_raw_accounting_data(
                            first_cell, second_cell, data, brother,great_brother)

                    # remember related cells
                    if brother:
                        great_brother = brother
                    brother = row
        except Exception as ex:
            error = ex.__class__.__name__
        return {
            'data': data,
            'error': error
        }
