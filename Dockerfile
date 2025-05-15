FROM python:3.10-slim

WORKDIR /app

COPY . .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "viewer.py"]