FROM gcr.io/google-appengine/python

ADD . /app/
WORKDIR /app
RUN ls
RUN virtualenv --python=python3.6 ./env
RUN ls
ENV VIRTUAL_ENV /app/env
ENV PATH /app/env/bin:$PATH
RUN ls
RUN whereis python
RUN whereis pip

RUN pip install -r requirements.txt
ENV FLASK_APP web.py
EXPOSE 5000/tcp
ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0"]
