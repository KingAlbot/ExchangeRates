FROM python:3.8.5

WORKDIR /app

COPY . .

RUN pip install pymysql requests

RUN . ./env_vars.sh

CMD ["daily_db_update.py"]

ENTRYPOINT ["python3"]


