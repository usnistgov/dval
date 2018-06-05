FROM python:3.6.5
#RUN pip install pip==9.0.3
RUN pip install pipenv

WORKDIR /src
#COPY requirements.txt /src/requirements.txt
#RUN pip install -r requirements.txt

COPY . /src/
RUN pipenv install --dev
ENTRYPOINT ["python", "-m d3m_outputs.cli"]
