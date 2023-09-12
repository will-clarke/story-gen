FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
# xecStart=/home/will/story-gen/venv/bin/gunicorn --workers 3 --bind unix:stories.sock -m 007 app:app
