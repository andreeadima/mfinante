import json
import flask
from flask import Flask
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait

import settings

app = Flask(__name__)


@app.route('/find/<year>/<cui>', methods=['GET', ])
def scrape_company(year, cui):
    my_url = settings.URL_PATH.format(settings.DOCUMENT_TEMPLATE.format(year),
                                      cui,
                                      settings.DOCUMENT_METHOD)
    scraper = CompanyDataScraper()
    data = scraper.scrape_link(my_url)
    return flask.jsonify(data)


class CompanyDataScraper():

    def __init__(self):
        self.driver = webdriver.PhantomJS()

    def scrape_link(self, url):
        desired_capabilities = dict(DesiredCapabilities.PHANTOMJS)
        self.driver.start_session(desired_capabilities)
        self.driver.get(url)
        data = {}
        try:
            WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element_by_tag_name(settings.ELEMENT_TAG))
            element = self.driver.find_element_by_tag_name(settings.ELEMENT_TAG)
            for row in element.find_elements_by_tag_name('tr'):
                if len(row.find_elements_by_tag_name('td')) == 2:
                    data[row.find_elements_by_tag_name('td')[0].text] = row.find_elements_by_tag_name('td')[1].text
        except TimeoutException:
            data = {'page': self.driver.page_source}
        return json.dumps(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
