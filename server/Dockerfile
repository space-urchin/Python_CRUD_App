FROM python:3.8

RUN pip install flask==1.1.2
RUN pip install Flask-SQLAlchemy==2.5.1
RUN pip install mysqlclient

COPY ./* /app/
COPY templates /app/templates
COPY static app/static
WORKDIR /app/

CMD ["python", "app.py"]