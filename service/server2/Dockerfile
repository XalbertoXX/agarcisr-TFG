FROM python:3.9-slim

# 1. Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Rust and Cargo
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:$PATH"

# 3. Working directory
WORKDIR /app

# 4. Copy code into the container
COPY . /app

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# 6. Expose port 5001
EXPOSE 5001

# 7. Run Flask server
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "f_server_2:app"]