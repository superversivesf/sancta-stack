# Bede Service

Liturgical calendar microservice using **romcal** (Node.js).

## Overview

Bede generates Catholic liturgical calendar data on-the-fly using the [romcal](https://github.com/romcal/romcal) TypeScript library. No pre-generated data files needed - romcal computes the calendar dynamically.

## Dependencies

- Node.js 20+
- [romcal](https://www.npmjs.com/package/romcal) ^1.4.0
- Express.js

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check |
| `GET /today` | Today's liturgical data |
| `GET /date/:date` | Specific date (YYYY-MM-DD) |
| `GET /year/:year` | Full year calendar |
| `GET /season/:season/:year` | Days in a season (advent, christmas, lent, eastertide, ordinary) |
| `GET /info` | Service information |

## Running

### Docker
```bash
docker-compose up -d bede
```

### Local Development
```bash
cd services/bede
npm install
npm start
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 3000 | HTTP port |

## About Romcal

Romcal is the official liturgical calendar library maintained by the Catholic Church's liturgical computing community. It handles:

- Easter date computation
- Moveable feasts
- Liturgical seasons
- Proper of Saints
- Local calendars

## License

MIT License
