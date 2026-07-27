### Build ###
FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim AS base

RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN node -v && npm -v

WORKDIR /app

COPY ./twisted .

### Deployment ###

ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy
ENV UV_TOOL_BIN_DIR=/usr/local/bin

EXPOSE 8000

RUN --mount=type=cache,target=/root/.cache/uv \
--mount=type=bind,source=uv.lock,target=uv.lock \
--mount=type=bind,source=pyproject.toml,target=pyproject.toml \
uv sync --locked --no-install-project

RUN uv run manage.py tailwind install
RUN uv run manage.py tailwind build
RUN uv run manage.py collectstatic --noinput

USER nonroot

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]

