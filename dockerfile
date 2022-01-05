FROM mcr.microsoft.com/playwright:focal


WORKDIR /usr/src/app
RUN mkdir -p /usr/src/app/output
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.12

RUN pip install "poetry==$POETRY_VERSION"
COPY pyproject.toml /usr/src/app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi
COPY . /usr/src/app/