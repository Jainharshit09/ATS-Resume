
FROM python:3.11-slim
WORKDIR /app
COPY requirment.txt .
RUN pip install -r requirment.txt
RUN pip install numpy==1.23.5 pandas==1.5.3
COPY . .
EXPOSE 8501
ENV PYTHONUNBUFFERED 1
CMD ["streamlit", "run", "app.py"]
