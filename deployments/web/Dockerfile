FROM gcr.io/google-appengine/python

RUN virtualenv --python=python3.6 env
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

ADD . /app/
WORKDIR /app
RUN pip install -r requirements.txt
ENV FLASK_APP web.py
EXPOSE 5000/tcp
ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0"]
