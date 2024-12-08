FROM python:3.12

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 3100

CMD ["/bin/bash", "-c", "prisma generate; gunicorn main:app -c gunicorn.conf.py"]