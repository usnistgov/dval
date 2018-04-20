FROM python:3.6.5-slim

COPY . /src/
WORKDIR /src

RUN pip install pip==9.0.3
RUN pip install .

ENTRYPOINT ["d3m_outputs"]

