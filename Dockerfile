FROM python:3.6.5-slim
RUN pip install pip==9.0.3

WORKDIR /src
COPY requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt

COPY . /src/
RUN pip install .

ENTRYPOINT ["d3m_outputs"]
