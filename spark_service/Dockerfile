FROM python:3.9-slim

# Install necessary tools and dependencies
USER root
RUN apt-get update && apt-get install -y \
    openjdk-17-jre-headless \
    procps \
    && apt-get clean

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Copy application code to container
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set the default command to run the Spark application
CMD ["python3", "spark_streaming.py"]
