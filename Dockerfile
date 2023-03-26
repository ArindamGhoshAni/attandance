FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE $PORT
CMD gunicorn --workers=1 --bind 0.0.0.0:$PORT app:app
