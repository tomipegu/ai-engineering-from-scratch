# Docker Architecture

This setup uses three services:

- `ai-dev` for CUDA, PyTorch, and Jupyter.
- `flask` for the API.
- `qdrant` as the vector database.

## Architecture

```text
                 ┌─────────────┐
                 │   Qdrant    │
                 │             │
                 │ 6333 / 6334 │
                 └──────┬──────┘
                       / \
                      /   \
                     /     \
           ai-qdrant       flask-qdrant
                  /           \
                 /             \
      ┌─────────▼────┐     ┌────▼────────┐
      │    ai-dev    │     │    Flask    │
      │              │     │             │
      │ CUDA         │     │ Flask API   │
      │ PyTorch      │     │ qdrant      │
      │ Jupyter      │     │ client      │
      │              │     │             │
      │ :8888        │     │ :5000       │
      └──────────────┘     └─────────────┘
```

## Why separate networks?

Docker Compose creates one shared default network if no custom networks are defined.

That would mean:

```text
ai-dev ↔ flask ↔ qdrant
```

All services could communicate with each other using their service names.

Instead, this project defines two networks:

```text
ai-qdrant
flask-qdrant
```

This gives us more control over service communication:

```text
ai-dev ↔ qdrant
flask  ↔ qdrant
ai-dev ✕ flask
```

`ai-dev` and `flask` cannot directly communicate because they do not share a network.

Qdrant belongs to both networks, so both services can reach it using:

```text
qdrant:6333
```

This improves isolation and makes the architecture explicit.

## Why use `depends_on`?

The Flask service contains:

```yaml
depends_on:
  - qdrant
```

This tells Docker Compose to start the Qdrant container before starting Flask.

The startup order becomes:

```text
Qdrant
  ↓
Flask
```

This is useful because Flask depends on Qdrant.

However, `depends_on` only controls startup order. It does not guarantee that Qdrant is already fully ready to accept requests. For that, a Docker health check can be added.

## Ports

```text
Jupyter → localhost:8888
Flask   → localhost:5000
Qdrant  → localhost:6333
```

Port `6334` is also exposed for Qdrant's gRPC interface.