FROM python:3.8-slim
RUN pip install connexion[swagger-ui]
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
RUN mkdir -p /var/www
COPY app /var/www
WORKDIR /var/www
ENV DB_HOST=172.17.0.1
ENV STORAGE_HOST=172.17.0.1
CMD python main.py
EXPOSE 5002
