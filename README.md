# Sancta Stack

A collection of local-first Catholic microservices for liturgy, scripture, catechetics, and prayer.

## Overview

Sancta Stack provides privacy-focused, self-hosted Catholic data services designed for individuals and parishes. Each service is a small, focused microservice that can run independently or as part of the complete stack.

## Services

| Service | Domain | Port | Description |
|---------|--------|------|-------------|
| `bede` | Liturgy | 3000 | Liturgical calendar (tempus-bede) ✅ |
| `scriptura` | Scripture | 3001 | Bible text, search, and semantic lookup |
| `doctrina` | Doctrine | 3002 | Catechisms (Baltimore, Trent) and teaching |
| `sancti` | Saints | 3003 | Hagiography and feast day information |
| `oratio` | Prayer | 3004 | Prayers, devotions, and the Rosary |

## Architecture

### Philosophy
- **Local-first**: All data and processing on your hardware
- **Open source**: Catholic public domain data where possible
- **Microservices**: Independent, composable services
- **Embedding-ready**: Semantic search across all services
- **Agent-friendly**: API-first design for AI assistants

### Tech Stack
- Docker containers
- Python/Flask or Dart/Shelf (TBD per service)
- SQLite or embedded JSON for data
- Vector search for semantic queries

## Getting Started

### Individual Services

Each service can be run independently:

```bash
cd services/bede
docker-compose up -d
```

### Full Stack

```bash
docker-compose up -d
```

## Data Sources

- **Bible**: CPDV, DRC, WEB-C (public domain)
- **Liturgical Calendar**: Romcal-based (public domain)
- **Catechism**: Baltimore Catechism #2 (public domain)
- **Saints**: Roman Martyrology tradition
- **Prayers**: Traditional Catholic prayers (public domain)

## License

MIT License - See LICENSE file

Data attribution noted per service.

## Related

- [sancta_via](https://github.com/superversivesf/sancta_via) - Catholic Flutter apps (parent project)
