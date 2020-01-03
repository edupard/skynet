# https://github.com/GoogleCloudPlatform/python-runtime
FROM

RUN virtualenv -p python3.6 /env

# activate environment
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# add source code
ADD . /app

# install requirements
RUN pip install -r /app/requirements.txt

# set working directory
WORKDIR /app

# run app
ENTRYPOINT ["python"]
