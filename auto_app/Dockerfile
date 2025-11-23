FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /auction_app


COPY req.txt /auction_app/
RUN pip install --upgrade pip && \
    pip install -r req.txt


COPY . /auction_app/
