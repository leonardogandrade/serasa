FROM python:3.13

WORKDIR /fastapi

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
