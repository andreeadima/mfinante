FROM debian:8.6

RUN apt-get update -y && apt-get install -y \
    python-pip \
    python-dev \
    python-lxml \
    build-essential \
    qt5-default \
    libqt5webkit5-dev \
    xvfb \
    git

RUN apt-get install -y libxml2-dev libxslt1-dev

RUN pip install --upgrade pip && pip install \
    lxml \
    xvfbwrapper \
    dryscrape

RUN mkdir mfinante
COPY . /mfinante/
WORKDIR mfinante

RUN pip install -U setuptools \
    && pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["scraper.py"]
