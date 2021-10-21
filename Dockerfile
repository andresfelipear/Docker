FROM python:3.9-alpine
ENV PYTHONUNBUFFERED=1


#directory creation process
RUN mkdir /code
WORKDIR /code
COPY . /code/

#install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt
