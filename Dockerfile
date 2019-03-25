FROM python:3.6

WORKDIR /src
COPY requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt

COPY . /src/
RUN python setup.py install

ENTRYPOINT ["python", "-m", "dval.cli"]

