FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "streamlit/app.py", "--server.address=0.0.0.0", "--server.port=8501"]