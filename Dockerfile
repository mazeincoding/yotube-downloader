FROM python:3.11

WORKDIR /app

# Install FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# For Windows compatibility, we'll use python -m uvicorn directly
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]