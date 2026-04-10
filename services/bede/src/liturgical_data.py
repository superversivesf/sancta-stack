"""
Liturgical Data Store

Embedded liturgical calendar data from sancta_via.
Based on Romcal 1.3.0 - covering 2024-2035 (12 years).
Data exported from sancta_via_liturgical_calendar.
"""

from datetime import date, timedelta
from typing import List, Optional, Dict, Any
import json
import os

class LiturgicalDataStore:
    """In-memory liturgical calendar data store using sancta_via data."""
    
    def __init__(self, data_path: str = None):
        """Initialize with data from JSON files."""
        self._data = {}
        self._index = {}
        
        if data_path is None:
            # Default to data directory relative to this file
            data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
        
        self._load_data(data_path)
    
    def _load_data(self, data_path: str):
        """Load liturgical calendar data from JSON files."""
        # Load index
        index_path = os.path.join(data_path, 'index.json')
        if os.path.exists(index_path):
            with open(index_path, 'r') as f:
                self._index = json.load(f)
        
        # Load combined data file
        combined_path = os.path.join(data_path, 'liturgical_calendar.json')
        if os.path.exists(combined_path):
            with open(combined_path, 'r') as f:
                self._data = json.load(f)
            print(f"✅ Loaded {len(self._data)} liturgical days from sancta_via")
        else:
            # Load individual year files
            for year in range(2024, 2036):
                year_file = os.path.join(data_path, f'liturgical_{year}.json')
                if os.path.exists(year_file):
                    with open(year_file, 'r') as f:
                        year_data = json.load(f)
                        self._data.update(year_data)
            print(f"✅ Loaded {len(self._data)} liturgical days")
    
    def get_day(self, query_date: date) -> Optional[Dict[str, Any]]:
        """Get liturgical data for a specific date."""
        date_str = query_date.isoformat()
        day_data = self._data.get(date_str)
        
        if day_data is None:
            return None
            
        # Add computed fields
        day_data['weekday'] = query_date.strftime('%A')
        return day_data
    
    def get_range(self, start: date, end: date) -> List[Dict[str, Any]]:
        """Get liturgical data for a date range."""
        days = []
        current = start
        while current <= end:
            day = self.get_day(current)
            if day:
                days.append(day)
            current += timedelta(days=1)
        return days
    
    def get_season_days(self, year: int, season: str) -> List[Dict[str, Any]]:
        """Get all days in a liturgical season."""
        season = season.lower()
        days = []
        
        for date_str, day_data in self._data.items():
            if day_data['year'] == year:
                day_season = day_data.get('season', '').lower()
                if season in day_season or day_season in season:
                    days.append(day_data)
        
        return sorted(days, key=lambda x: x['date'])
    
    def get_feasts(self, year: int, days_ahead: int = 30) -> List[Dict[str, Any]]:
        """Get upcoming feasts and solemnities from today."""
        start = date.today()
        end = start + timedelta(days=days_ahead)
        days = self.get_range(start, end)
        
        # Filter for feasts, solemnities, memorials
        feast_types = ['SOLEMNITY', 'FEAST', 'MEMORIAL']
        return [d for d in days 
                if d.get('celebration', {}).get('type') in feast_types
                or d.get('celebration', {}).get('prioritized', False)]
    
    def get_year_days(self, year: int) -> List[Dict[str, Any]]:
        """Get all liturgical days for a year."""
        return [day for day in self._data.values() if day.get('year') == year]
    
    def available_years(self) -> List[int]:
        """Return list of available years."""
        if self._index and 'years' in self._index:
            return [y['year'] for y in self._index['years']]
        return list(range(2024, 2036))
    
    def get_year_range(self) -> Dict[str, int]:
        """Return available year range."""
        years = sorted(self.available_years())
        if years:
            return {'start': years[0], 'end': years[-1]}
        return {'start': 2024, 'end': 2035}
    
    def search_celebrations(self, query: str) -> List[Dict[str, Any]]:
        """Search celebrations by name."""
        query = query.lower()
        results = []
        
        for day_data in self._data.values():
            celebration = day_data.get('celebration', {})
            name = celebration.get('name', '').lower()
            if query in name:
                results.append(day_data)
        
        return sorted(results, key=lambda x: x['date'])
