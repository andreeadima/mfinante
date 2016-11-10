from flask import Flask
import dryscrape
from bs4 import BeautifulSoup
import time
import settings
import json

app = Flask(__name__)

@app.route('/find/<year>/<cui>/<table_nr>', methods=['GET', ])
def get_company_data(year, cui, table_nr):
    dryscrape.start_xvfb()
    session = dryscrape.Session()
    my_url = settings.URL_PATH.format(settings.DOCUMENT_TEMPLATE.format(year),
                                      cui,
                                      settings.DOCUMENT_METHOD)
    session.set_attribute('auto_load_images', False)
    session.visit(my_url)
    time.sleep(5)

    response = session.body()
    soup = BeautifulSoup(response, "lxml")
    data = {'response': str(response),
            'url': my_url}
    tables = soup.findAll('table')
    if tables and len(tables) > table_nr:
        data['table'] = str(table)
    return json.dumps(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
