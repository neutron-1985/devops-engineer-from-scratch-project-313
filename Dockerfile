FROM python:3.14-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PATH="/root/.local/bin:${PATH}"


RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates curl make nginx nodejs npm && \
    rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

COPY package.json package-lock.json ./
RUN npm ci --omit=dev

COPY . .

RUN mkdir -p /app/public && \
    cp -r ./node_modules/@hexlet/project-devops-deploy-crud-frontend/dist/. /app/public/

COPY nginx.conf /etc/nginx/sites-available/default

EXPOSE 80

CMD ["bin/start.sh"]
