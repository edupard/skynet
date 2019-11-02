FROM gcr.io/google-appengine/python

RUN virtualenv -p python3.7 /env

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

RUN pip --version
RUN whereis python

ADD . /app

RUN pip install -r /app/requirements.txt

RUN whereis flask

ENV FLASK_APP web.py
EXPOSE 5000/tcp
ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0"]
