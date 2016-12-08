# Mfinante scraper

Description:
------------

Dockerized application to get data from mfinante.ro about companies.


Installation
------------

1. Install [Docker](https://www.docker.com).

2. Install [Docker Compose](https://docs.docker.com/compose/).


Run project:
------------

1. Start a new container from image:

    ``` 
    docker-compose up
    ```
    
2. Project is up and running at:

    ```
    http://<host>:5000/find?cui=<cui>&year=<year>
    ```

Exposed URLS:
-------------

1. Get raw data - params: cui, year

    ```
    http://<host>:5000/find-raw?cui=<cui>&year=<year>
    ```

2. Get accounting data - params: cui, year
 
    ```
    http://<host>:5000/find?cui=<cui>&year=<year>
    ```
 
 
JSON structure:
---------------

1. Request:
    * cui 
    * year
    * url - url built from params
    
2. Response:
    * success - boolean
    * result - dict containing company data 
    * error - string containing error class if any error occured
    
