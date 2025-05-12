FROM python:3.13.3

WORKDIR /app

RUN pip install -r requirements/requirements.txt

COPY . .

RUN cd src

CMD ["python", "main.py"]