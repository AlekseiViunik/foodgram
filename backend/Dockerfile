FROM python:3.10-slim

WORKDIR /app

COPY . ./

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]
