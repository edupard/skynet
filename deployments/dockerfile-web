# https://github.com/GoogleCloudPlatform/python-runtime
FROM gcr.io/google-appengine/python

RUN virtualenv -p python3.6 /env

# activate environment
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# add source ode
ADD . /app

# install requirements
RUN pip install -r /app/requirements.txt

# set working directory
WORKDIR /app

# run app
ENV FLASK_APP web.py
EXPOSE 5000/tcp
ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0"]
