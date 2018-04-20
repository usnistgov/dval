FROM python:3.6.5-slim

COPY . /src/

RUN pip install pip==9.0.3
RUN pip install /src

ENTRYPOINT ["d3m_outputs"]

