# Use the official NVIDIA CUDA image as the base image
FROM nvidia/cuda:9.0-cudnn7-runtime-ubuntu16.04

# Set the working directory inside the container
WORKDIR /app

# Install dependencies for building Python
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libffi-dev \
    zlib1g-dev \
    python3-pip \
    python3-dev

# Download and install Python 3.6.13
RUN wget https://www.python.org/ftp/python/3.6.13/Python-3.6.13.tgz && \
    tar -xzf Python-3.6.13.tgz && \
    cd Python-3.6.13 && \
    ./configure --enable-optimizations && \
    make -j $(nproc) && \
    make altinstall && \
    cd ..

# Create a symlink for python3.6
RUN ln -s /usr/local/bin/python3.6 /usr/bin/python3

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip3 install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the application will run on
EXPOSE 8000

# Command to run the application
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
