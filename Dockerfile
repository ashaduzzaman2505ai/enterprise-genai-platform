FROM python:3.10-slim

WORKDIR /app

# Disable CUDA for torch to avoid CUDA library loading issues
ENV CUDA_VISIBLE_DEVICES=""

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install -e .

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
