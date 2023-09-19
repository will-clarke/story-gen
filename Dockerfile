FROM python:3.9

WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000","app:app" ]
# gunicorn --bind 0.0.0.0:5000 app:app
