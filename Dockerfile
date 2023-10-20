FROM python:3.11-alpine
COPY . /app
WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt
CMD ["/bin/bash", "/scripts/create-interfaces.sh"]
CMD ["/bin/bash", "/scripts/update-toml.sh"]
CMD ["python3", "main.py"]
