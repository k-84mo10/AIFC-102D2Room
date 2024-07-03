# Dockerfile
FROM python:3.8-slim

WORKDIR /app

# Set timezone
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libopencv-dev \
        && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install torch==2.3.1 torchvision==0.18.1 opencv-python==4.9.0.80 pyserial==3.5

CMD ["tail", "-f", "/dev/null"]
