from company_scraper import CompanyDataScraper

import flask
import settings

app = flask.Flask(__name__)


def scrape_company(year, cui, raw=False):
    my_url = settings.URL_PATH.format(settings.DOCUMENT_TEMPLATE.format(year),
                                      cui,
                                      settings.DOCUMENT_METHOD)
    scraper = CompanyDataScraper()
    if raw:
        scraper_result = scraper.scrape_raw_data(my_url)
    else:
        scraper_result = scraper.scrape_pretty_data(my_url)
    response = {
        'request': {
            'cui': cui,
            'year': year,
            'url': my_url,
        },
        'response': {
            'success': False if scraper_result['error'] else True,
            'result': scraper_result['data'],
            'error': scraper_result['error']
        }
    }
    return response


# Scrape mfinante and get data in accounting format
@app.route('/find', methods=['GET', ])
def scrape_company_pretty():
    year = flask.request.args['year']
    cui = flask.request.args['cui']
    response = scrape_company(year, cui)
    return flask.jsonify(response)


# Scrape mfinante and get data in raw format
@app.route('/find-raw', methods=['GET', ])
def scrape_company_raw():
    year = flask.request.args['year']
    cui = flask.request.args['cui']
    response = scrape_company(year, cui, raw=True)
    return flask.jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
