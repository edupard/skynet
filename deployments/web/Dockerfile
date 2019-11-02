FROM gcr.io/google-appengine/python

RUN virtualenv -p python3.6 /env

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

ADD . /app

RUN pip install -r /app/requirements.txt

WORKDIR /app
RUN pwd & ls & pip --version & whereis flask
ENV FLASK_APP web.py
EXPOSE 5000/tcp
ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0"]
