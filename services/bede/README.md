# Bede Service

Liturgical calendar microservice providing Catholic liturgical date information.

## Overview

Bede is a compatible reimplementation of [tempus-bede](https://github.com/geno7/tempus-bede) using embedded data from the [sancta_via](https://github.com/superversivesf/sancta_via) liturgical calendar package.

## Data Source

- **Source**: sancta_via_liturgical_calendar (Romcal 1.3.0)
- **Coverage**: 2024-2035 (12 years)
- **Total Days**: 4,383 liturgical days
- **Celebrations**: 856 prioritized celebrations

## API Endpoints

### Standard (tempus-bede compatible)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/today` | GET | Today's liturgical data |
| `/date/:date` | GET | Specific date (YYYY-MM-DD) |

### Extended

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/range/:start/:end` | GET | Date range query |
| `/season/:season/:year` | GET | All days in a season |
| `/feasts/:year` | GET | Upcoming feasts and solemnities |
| `/info` | GET | Service information |

## Response Format

```json
{
  "date": "2025-04-10",
  "id": "easter-triduum-holy-thursday",
  "name": "Holy Thursday",
  "rank": "SOLEMNITY",
  "season": "easter-triduum",
  "color": ["white"],
  "isFeast": true,
  "isSolemnity": true,
  "meta": {
    "cycle": "C",
    "weekday": "Thursday"
  }
}
```

## Running

### Docker (recommended)
```bash
docker-compose up -d bede
```

### Development
```bash
cd services/bede
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd src
python -m flask app --port 3000
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 3000 | HTTP port |
| `BEDE_DIOCESE` | united-states | Default diocese/calendar |
| `DEBUG` | false | Flask debug模式 |

## Status

⚠️ **Work in Progress**: Currently using placeholder data. Integration with actual sancta_via liturgical data is pending.

## License

MIT License - See top-level LICENSE file
