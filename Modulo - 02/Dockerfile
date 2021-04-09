FROM python:3.7

COPY . /app
WORKDIR /app

RUN apt-get -y update && apt-get install -y gnupg2 wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update

RUN apt-get install -y --no-install-recommends \
    ca-certificates \
    cmake \
    build-essential \
    gcc \ 
    g++ \
    unzip \
    google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Run the image as a non-root user
#RUN adduser -D myuser
#USER myuser

ARG PORT=80
ARG TIMEOUT=300

# set display port to avoid crash
ENV PORT $PORT
ENV TIMEOUT $TIMEOUT
ENV DISPLAY=:99

RUN pip install -r requirements.txt
RUN python db_starter.py

#CMD python ./app.py
CMD gunicorn --bind 0.0.0.0:$PORT -t $TIMEOUT wsgi