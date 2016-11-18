FROM debian:8.6

RUN apt-get update -y && apt-get install -y \
    python-pip python-dev git \
    build-essential libfontconfig

RUN pip install --upgrade pip
RUN cd /usr/local/share
RUN apt-get install -y curl
RUN curl -L -o phantomjs-2.1.1-linux-x86_64.tar.bz2  \
    https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 && \
    tar xvjf phantomjs-2.1.1-linux-x86_64.tar.bz2 && \
    mv phantomjs-2.1.1-linux-x86_64 /usr/local/share && \
    ln --force -s /usr/local/share/phantomjs-2.1.1-linux-x86_64 /usr/local/share/phantomjs && \
    ln --force -s /usr/local/share/phantomjs/bin/phantomjs /usr/local/bin/phantomjs
RUN ls /usr/local/share/phantomjs/bin | grep phantom
RUN phantomjs --version

RUN mkdir mfinante
COPY ./scraper /mfinante/
WORKDIR mfinante

RUN pip install -U setuptools \
    && pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["scraper.py"]
