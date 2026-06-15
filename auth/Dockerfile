FROM python:3.12-slim

WORKDIR /auth

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7000", "--reload"]
