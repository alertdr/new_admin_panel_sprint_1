FROM python:3.10.2-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm requirements.txt

COPY *.py .
COPY db.sqlite .
COPY movies_database.ddl .

EXPOSE 5432:5432

ENTRYPOINT ["python", "./load_data.py"]
