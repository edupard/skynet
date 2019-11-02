FROM gcr.io/google-appengine/python

RUN virtualenv --python=python3.6 env

ADD . /app/

ENV VIRTUAL_ENV ./app/env
ENV PATH ./app/env/bin:$PATH

WORKDIR /app

RUN pip --version
RUN pip install -r requirements.txt
ENV FLASK_APP web.py
EXPOSE 5000/tcp
ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0"]
