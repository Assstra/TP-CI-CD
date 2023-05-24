FROM python:3.10-alpine

COPY ./requirements.txt /app/requirements.txt

# set workdir to app
WORKDIR /app

# install dependencies
RUN pip install -r requirements.txt

# Copy app folder
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["application.py" ]