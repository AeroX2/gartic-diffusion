FROM python as python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1

FROM python-base as poetry
WORKDIR /workdir
RUN pip3 install poetry
RUN python -m venv --copies venv
COPY pyproject.toml poetry.lock ./
RUN . venv/bin/activate && poetry install --no-dev --no-interaction --no-ansi -vvv

FROM python-base
WORKDIR /workdir
COPY --from=poetry /workdir/venv /workdir/venv
ENV PATH /workdir/venv/bin:$PATH
COPY . ./

WORKDIR /workdir/src
CMD ["python", "app.py"]
EXPOSE 5000