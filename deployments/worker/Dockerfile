FROM gcr.io/google-appengine/python

ADD . /app/

RUN virtualenv --python=python3.6 env
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH


WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["worker.py"]
