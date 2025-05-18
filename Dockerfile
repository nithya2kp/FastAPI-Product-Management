FROM python:3.13-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /shopalyst
COPY requirements.txt /shopalyst/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY shopalyst_fastapi/ /shopalyst/backend/
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]