# Use a slim, stable Python image commonly used in industry for data work
FROM python:3.11-slim

# Disable interactive prompts during apt installs
ENV DEBIAN_FRONTEND=noninteractive

# Install essential system packages and build tools
# - build-essential: needed to compile Python packages (e.g., pandas)
# - libffi/libssl: required by dbt and Google libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    wget \
    unzip \
    libffi-dev \
    libssl-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and wheel for smoother installs
RUN pip install --upgrade pip setuptools wheel

# Install core Python libraries:
# - dbt-bigquery: transformation layer
# - pandas, requests: for ingestion/ETL scripting
# (You can add others here later, like pyarrow or jinja2 if needed)
RUN pip install dbt-bigquery pandas requests

# Create a non-root user for better security (best practice)
RUN useradd -ms /bin/bash devuser

# Switch to non-root user
USER devuser

# Set working directory inside the container
WORKDIR /home/devuser

# By default, open a shell so you can work interactively
CMD ["bash"]
