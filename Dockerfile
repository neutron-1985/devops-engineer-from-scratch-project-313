FROM ubuntu

ENV DEBIAN_FRONTEND=noninteractive \
    PATH="/root/.local/bin:${PATH}" \
    APP_HOST=0.0.0.0 \
    APP_PORT=8080

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates curl make python3 && \
    rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN uv python install 3.14

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

COPY . .

EXPOSE 8080

CMD ["bin/start.sh"]
