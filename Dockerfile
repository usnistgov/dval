FROM python:3.6.5
RUN pip install pip==9.0.3
#RUN pip install pipenv

WORKDIR /src
COPY requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt && \
    pip install --process-dependency-links git+https://gitlab.com/datadrivendiscovery/d3m.git@v2018.6.5#egg=d3m

#COPY Pipfile /src/Pipfile
#RUN pipenv install --dev && pipenv install --system --dev

COPY . /src/
RUN python setup.py install

ENTRYPOINT ["python", "-m", "d3m_outputs.cli"]

