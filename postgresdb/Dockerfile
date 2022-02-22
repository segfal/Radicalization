FROM postgres:13
ENV POSTGRES_PASSWORD H5pME2DfJPtvuSJM
ENV POSTGRES_USER postgres
ENV POSTGRES_DB social_network
RUN apt update && apt upgrade
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install build-essential
RUN apt  install -y libglib2.0-dev libpq-dev
WORKDIR db_code
COPY requirements.txt requirements.txt
COPY implementation implementation
COPY plusminus.xlsx plusminus.xlsx
RUN pip3 install -r requirements.txt
RUN python3 -m spacy download en_core_web_sm
RUN python3 -m spacy download en_core_web_md
