# Mfinante scraper

Description:
------------

Dockerized application to get data from mfinante.ro about companies.

Exposed URLS:
-------------

1. Get raw data :

    ```
    http://<host>:5000/find/<year>/<cui>/raw 
    ```

2. Get accounting data:
 
    ```
    http://<host>:5000/find/<year>/<cui>/raw
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
    

System prerequisites:
---------------------

1. Install docker:

  ```
  sudo apt-get install docker-engine
  ```
  

Project installation:
---------------------

1. Start docker service:

  ```
  sudo service docker start
  ```

2. Build image from docker file (will take a while):

  ```
  sudo docker build . -t mfinante
  ```


Run project:
------------

1. Start docker service:

  ```
  sudo service docker start
  ```

2. Start a new container from image:

    ``` 
    docker run -d -p 5000:5000 mfinante    
    ```
    
3. Project is up and running at:

    ```
    http://<host>:5000
    ```
