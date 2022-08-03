FROM python:3.9.13-bullseye

COPY ./ /webserver

WORKDIR /webserver

RUN pip install -r requirements.txt

RUN chmod +x start-server.sh

RUN chmod +x wait-for-it.sh

EXPOSE 8000

CMD ./start-server.sh


