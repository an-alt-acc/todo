FROM python:alpine
EXPOSE 5000
WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT [ "python" ]
CMD [ "app.py" ]