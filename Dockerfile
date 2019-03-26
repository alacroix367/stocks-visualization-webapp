FROM heroku/miniconda
#FROM alpine:latest

# Grab requirements.txt.
ADD ./webapp/requirements.txt /tmp/requirements.txt

# Install dependencies
RUN pip install -qr /tmp/requirements.txt

# Add our code
ADD ./webapp /opt/webapp/
WORKDIR /opt/webapp

RUN conda install bokeh
RUN conda install pandas
RUN conda install numpy
RUN conda install requests
RUN conda install simplejson

CMD gunicorn --bind 0.0.0.0:$PORT wsgi