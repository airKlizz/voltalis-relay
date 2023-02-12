FROM python:3.10-alpine
EXPOSE 80
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN mkdir /code/app
COPY ./app/voltalis.py /code/app/voltalis.py
COPY ./app/main.py /code/app/main.py
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]