FROM python:3.10-slim

WORKDIR /app

COPY ./main.py /app/main.py
COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]