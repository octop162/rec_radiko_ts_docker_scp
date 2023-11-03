FROM python:bullseye

WORKDIR /work
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libxml2-utils \
        curl \
        ca-certificates \
        ffmpeg \
        sshpass \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

RUN curl "https://raw.githubusercontent.com/uru2/rec_radiko_ts/master/rec_radiko_ts.sh" -o rec_radiko_ts.sh \
    && chmod +x rec_radiko_ts.sh 

COPY ./requirements.txt /work/requirements.txt
COPY ./app.py /work/app.py
RUN pip install -r requirements.txt

CMD [ "python", "app.py" ]
