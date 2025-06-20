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

# Install bq CLI
RUN apt-get update && apt-get install -y \
    lsb-release \
    gnupg \
    && echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - \
    && apt-get update && apt-get install -y google-cloud-sdk

# Upgrade pip and wheel for smoother installs
RUN pip install --upgrade pip setuptools wheel

# Install core Python libraries:
# - dbt-bigquery: transformation layer
# - pandas, requests: for ingestion/ETL scripting
# (You can add others here later, like pyarrow or jinja2 if needed)
RUN pip install \
    dbt-bigquery \
    pandas \
    requests \
    jupyter \
    notebook \
    ipykernel \
    python-dotenv \
    google-cloud-storage

# Create a non-root user for better security (best practice)
RUN useradd -ms /bin/bash devuser

# Switch to non-root user
USER devuser

# Set working directory inside the container
WORKDIR /home/devuser

# Register the kernel so VS Code can detect it
RUN python3 -m ipykernel install --user \
    --name=daily_insights_env \
    --display-name="Python 3.11 (Daily Insights)"
    
# By default, open a shell so you can work interactively
CMD ["bash"]
