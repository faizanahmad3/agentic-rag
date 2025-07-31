# Use lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

## Expose port (for Streamlit or FastAPI)
#EXPOSE 8501
#
## Default command (run Streamlit or FastAPI later)
#CMD ["streamlit", "run", "src/ui/app.py"]
