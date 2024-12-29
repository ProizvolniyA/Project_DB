FROM postgres:latest

LABEL author="armenmk"
LABEL description="Purchase Database"
LABEL version="1.0"

COPY *.sql /docker-entrypoint-initdb.d/
