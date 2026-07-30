### Build ###
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS development

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

WORKDIR /app

COPY ./twisted .

ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy
ENV UV_TOOL_BIN_DIR=/usr/local/bin
ENV HOME=/tmp
ENV XDG_CACHE_HOME=/tmp/.cache
ENV UV_CACHE_DIR=/tmp/uv-cache

# ARG POSTGRES_DB=twisted
# ARG POSTGRES_USER=twisted
# ARG POSTGRES_PASSWORD=twisted
# ARG POSTGRES_HOST=localhost
# ARG HCA_CLIENT_ID=build-client-id
# ARG HCA_CLIENT_SECRET=build-client-secret
# ARG HCA_REDIRECT_URI=http://localhost:8000/oauth/callback/
# ARG DEFAULT_PFP=https://example.com/default-pfp.png
# ARG HACKATIME_CLIENT_ID=build-hackatime-client-id
# ARG HACKATIME_CLIENT_SECRET=build-hackatime-client-secret
# ARG HACKATIME_REDIRECT_URI=http://localhost:8000/oauth/hackatime_callback/

RUN --mount=type=cache,target=/root/.cache/uv \
--mount=type=bind,source=uv.lock,target=uv.lock \
--mount=type=bind,source=pyproject.toml,target=pyproject.toml \
uv sync --locked --no-install-project

# RUN export POSTGRES_DB="$POSTGRES_DB" \
#     POSTGRES_USER="$POSTGRES_USER" \
#     POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
#     POSTGRES_HOST="$POSTGRES_HOST" \
#     HCA_CLIENT_ID="$HCA_CLIENT_ID" \
#     HCA_CLIENT_SECRET="$HCA_CLIENT_SECRET" \
#     HCA_REDIRECT_URI="$HCA_REDIRECT_URI" \
#     DEFAULT_PFP="$DEFAULT_PFP" \
#     HACKATIME_CLIENT_ID="$HACKATIME_CLIENT_ID" \
#     HACKATIME_CLIENT_SECRET="$HACKATIME_CLIENT_SECRET" \
#     HACKATIME_REDIRECT_URI="$HACKATIME_REDIRECT_URI"

RUN uv run manage.py tailwind install
RUN uv run manage.py tailwind build
RUN uv run manage.py collectstatic --noinput
RUN uv run manage.py migrate


RUN mkdir -p /tmp/uv-cache /tmp/.cache \
 && chown -R 999:999 /tmp/uv-cache /tmp/.cache

### Deployment ###

EXPOSE 8000

USER 999:999

CMD ["uv", "run", "gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]

