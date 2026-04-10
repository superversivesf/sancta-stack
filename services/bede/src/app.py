"""
Bede Service - Liturgical Calendar API

A compatible reimplementation of tempus-bede using sancta_via liturgical data.
Provides Catholic liturgical calendar information via REST API.

API compatibility with tempus-bede:
- GET /health - Health check
- GET /today - Today's liturgical data
- GET /date/:date - Specific date data (YYYY-MM-DD)

Additional endpoints:
- GET /range/:start/:end - Date range query
- GET /season/:season/:year - All days in a season
- GET /feasts/:year - Upcoming feasts and solemnities
- GET /search - Search celebrations by name
"""

from flask import Flask, jsonify, request
from datetime import datetime, date
from liturgical_data import LiturgicalDataStore
import os

app = Flask(__name__)
data_store = LiturgicalDataStore()

DEFAULT_DIOCESE = os.environ.get('BEDE_DIOCESE', 'united-states')


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'service': 'bede',
        'version': '1.0.0',
        'data_source': 'sancta_via_liturgical_calendar (Romcal 1.3.0)',
        'data_years': data_store.available_years()
    })


@app.route('/today')
def today():
    """Get liturgical data for today."""
    result = data_store.get_day(date.today())
    if result is None:
        return jsonify({
            'error': 'Date out of range',
            'available_range': data_store.get_year_range()
        }), 404
    return jsonify(_format_response(result))


@app.route('/date/<date_str>')
def get_date(date_str):
    """Get liturgical data for a specific date (YYYY-MM-DD)."""
    try:
        query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    result = data_store.get_day(query_date)
    if result is None:
        return jsonify({
            'error': f'Date {date_str} out of range',
            'available_range': data_store.get_year_range()
        }), 404
    
    return jsonify(_format_response(result))


@app.route('/range/<start_date>/<end_date>')
def get_range(start_date, end_date):
    """Get liturgical data for a date range."""
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    if start > end:
        return jsonify({'error': 'Start date must be before end date'}), 400
    
    results = data_store.get_range(start, end)
    return jsonify({
        'start': start_date,
        'end': end_date,
        'days': [_format_response(day) for day in results],
        'count': len(results)
    })


@app.route('/season/<season>/<int:year>')
def get_season(season, year):
    """Get all days in a liturgical season for a given year."""
    season = season.lower()
    valid_seasons = ['advent', 'christmas', 'lent', 'eastertide', 'easter', 'ordinary', 'holy-week']
    
    if season not in valid_seasons:
        return jsonify({
            'error': f'Invalid season. Must be one of: {valid_seasons}'
        }), 400
    
    days = data_store.get_season_days(year, season)
    if not days:
        return jsonify({'error': f'No data for year {year}'}), 404
    
    return jsonify({
        'season': season,
        'year': year,
        'days': [_format_response(day) for day in days],
        'count': len(days)
    })


@app.route('/feasts/<int:year>')
def get_feasts(year):
    """Get upcoming feasts and solemnities."""
    days_ahead = request.args.get('days', 30, type=int)
    
    feasts = data_store.get_feasts(year, days_ahead)
    return jsonify({
        'year': year,
        'days_ahead': days_ahead,
        'feasts': [_format_response(day) for day in feasts],
        'count': len(feasts)
    })


@app.route('/search')
def search():
    """Search celebrations by name."""
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Query parameter "q" required'}), 400
    
    results = data_store.search_celebrations(query)
    return jsonify({
        'query': query,
        'results': [_format_response(day) for day in results],
        'count': len(results)
    })


@app.route('/info')
def info():
    """Service information."""
    return jsonify({
        'service': 'bede',
        'name': 'Sancta Stack - Liturgical Calendar Service',
        'version': '1.0.0',
        'description': 'Catholic liturgical calendar data from sancta_via',
        'endpoints': [
            '/health',
            '/today',
            '/date/:date',
            '/range/:start/:end',
            '/season/:season/:year',
            '/feasts/:year',
            '/search?q=query',
            '/info'
        ],
        'data_source': 'sancta_via_liturgical_calendar (Romcal 1.3.0)',
        'data_range': data_store.get_year_range(),
        'total_days': len(data_store._data) if hasattr(data_store, '_data') else 0
    })


def _format_response(day_data):
    """Format day data to match tempus-bede API."""
    celebration = day_data.get('celebration', {})
    
    return {
        'date': day_data['date'],
        'id': celebration.get('key', 'weekday'),
        'name': celebration.get('name', 'Weekday'),
        'rank': celebration.get('type', 'FERIA'),
        'season': day_data.get('season', 'Ordinary'),
        'color': [celebration.get('color', 'green')],
        'isFeast': celebration.get('type') in ['FEAST', 'SOLEMNITY', 'MEMORIAL'],
        'isSolemnity': celebration.get('type') == 'SOLEMNITY',
        'isOptional': celebration.get('type') == 'OPT_MEMORIAL',
        # Additional metadata
        'meta': {
            'cycle': 'C',  # Would extract from actual data
            'weekday': day_data.get('weekday', ''),
            'weekOfSeason': 1,  # Would extract from actual data
            'prioritized': celebration.get('prioritized', False)
        }
    }


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
