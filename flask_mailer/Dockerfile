FROM python:3

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app
COPY ./ /app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py", "-h" "192.168.0.1"]
