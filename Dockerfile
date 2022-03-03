FROM python:3.10-alpine

RUN /usr/local/bin/python -m pip install --upgrade pip && pip install pipenv

ENV PROJECT_DIR /usr/local/bin/src/log_output

WORKDIR ${PROJECT_DIR}

COPY Pipfile* ${PROJECT_DIR}/

RUN pipenv install --system --deploy

COPY main.py .

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "3001"]
