FROM python:3.6.5-slim
COPY . /src/
RUN pip install /src

ENTRYPOINT ["d3m_outputs"]

