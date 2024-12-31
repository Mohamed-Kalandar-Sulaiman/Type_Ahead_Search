FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY ./src /app/src

# Expose port 80
EXPOSE 80

CMD ["./run.sh"]
