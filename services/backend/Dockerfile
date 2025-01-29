FROM python:3.10

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

RUN chmod +x ./entrypoint/backend.sh && chmod +x ./entrypoint/wait-for-it.sh && chmod +x ./entrypoint/worker.sh

ENTRYPOINT ["./entrypoint/backend.sh"]