FROM python:alpine
EXPOSE 5000
WORKDIR /app

COPY requirements/prod.txt ./requirements/prod.txt
RUN pip install -r requirements/prod.txt
COPY . .

ENTRYPOINT [ "python" ]
CMD [ "app.py" ]