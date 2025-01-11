
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Expose the port that Streamlit uses by default
EXPOSE 8501
CMD ["streamlit", "run", "streamlit.py"]
