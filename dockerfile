FROM python:3.10

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "restarter.py"]