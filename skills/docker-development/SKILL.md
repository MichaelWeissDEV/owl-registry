---
name: docker-development
description: >
  Build, optimize, run, and orchestrate containerized applications using Docker
  and Docker Compose. Use when writing efficient multi-stage Dockerfiles, optimizing
  image layer caching, configuring docker-compose services and networks, managing
  persistent volumes, or setting up reproducible local development containers.
compatibility: >
  Agent Skills-compatible coding agents operating with Docker and Docker Compose.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "docker, containers, dockerfile, compose, multi-stage, devops"
  topics: "devops, devtools, software-development"
---

# Modern Docker Development & Compose

Docker provides lightweight container virtualization, ensuring identical execution environments across local development, CI/CD pipelines, and production clusters. High-performance Docker workflows leverage multi-stage builds, aggressive layer caching, non-root user execution, and clean compose service boundaries.

## Core Rules

1. **Always use Multi-Stage Builds**: Compile code, install build compilers, and fetch dependencies in builder stages; copy only the final minimal binary/artifacts into the runtime image.
2. **Order instructions by volatility for layer caching**: Place rarely-changing instructions (system package installs, dependency manifests) before frequently-changing source code copies.
3. **Always run as an unprivileged user**: Never leave `USER root` active in the final production runtime container. Create and switch to a dedicated user (`appuser`).
4. **Use explicit `.dockerignore` files**: Prevent local `.git/`, `node_modules/`, `.venv/`, temporary caches, and `.env` secret files from inflating the build context.
5. **Pin base image tags**: Avoid `:latest`. Pin major or minor versions (e.g. `python:3.11-slim-bookworm`, `node:20-alpine`) to guarantee reproducible builds.

---

## 1. Canonical Multi-Stage Dockerfile (Python / Node / Go)

Example: Python application with compiled C-extensions using `uv`:

```dockerfile
# ==============================================================================
# Stage 1: Build & Dependency Resolution
# ==============================================================================
FROM python:3.11-slim-bookworm AS builder

# Install build tools needed for native extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy only dependency manifests first to leverage layer cache
COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir build wheel && \
    python -m build --wheel --outdir /dist

# ==============================================================================
# Stage 2: Minimal Production Runtime
# ==============================================================================
FROM python:3.11-slim-bookworm AS runner

# Create dedicated unprivileged user and group
RUN groupadd -r -g 1001 appgroup && \
    useradd -r -u 1001 -g appgroup -d /app -s /sbin/nologin appuser

WORKDIR /app

# Copy built wheels from builder stage
COPY --from=builder /dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && rm -rf /tmp/*.whl

# Switch to unprivileged runtime user
USER appuser:appgroup

# Metadata and execution
EXPOSE 8080
ENV PYTHONUNBUFFERED=1 \
    PORT=8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health', timeout=2)" || exit 1

ENTRYPOINT ["python", "-m", "my_app.server"]
```

---

## 2. Essential `.dockerignore`

Place in the root directory alongside the Dockerfile:

```gitignore
.git
.github
.gitignore
.venv
node_modules
__pycache__
*.pyc
*.pyo
dist
build
*.egg-info
.coverage
.pytest_cache
.env
.env.*
Dockerfile*
docker-compose*.yml
README.md
docs/
```

---

## 3. Multi-Service Local Development with Docker Compose

Modern `docker-compose.yml` (Compose specification format):

```yaml
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
      target: runner
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgres://app:secret@db:5432/app_db
      - REDIS_URL=redis://redis:6379/0
      - LOG_LEVEL=DEBUG
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - app-net

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: app_db
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d app_db"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - app-net

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    networks:
      - app-net

volumes:
  pgdata:

networks:
  app-net:
    driver: bridge
```

---

## 4. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| `COPY . .` before installing dependencies | Every code edit invalidates dependency layer cache | Copy `package.json` / `pyproject.toml` first, install, then copy source |
| Running container as `root` | Container breakout grants attacker root access to host OS | Add `USER appuser` in final stage |
| Baking secrets via `ENV API_KEY=xyz` | Secret is permanently visible in image history (`docker history`) | Inject secrets dynamically at runtime |
| Missing `rm -rf /var/lib/apt/lists/*` | Bloats final image size by 50-100MB with package index caches | Always clean apt caches in the same `RUN` command |

---

## 5. Verification Checklist

- [ ] `.dockerignore` exists and excludes `.git`, `.env`, and local dependencies.
- [ ] Multi-stage build isolates build compilers from production runtime.
- [ ] Container runs as an explicit non-root `USER`.
- [ ] Layer caching verified (rebuilding after code edit does not re-install dependencies).
- [ ] Compose services include health checks and explicit network definitions.
