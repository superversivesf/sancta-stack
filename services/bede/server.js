const express = require('express');
const Romcal = require('romcal').default;

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    service: 'bede',
    version: '1.0.0',
    romcal_version: '1.4.0'
  });
});

// Service info
app.get('/info', (req, res) => {
  res.json({
    service: 'bede',
    name: 'Sancta Stack - Liturgical Calendar Service',
    version: '1.0.0',
    description: 'Catholic liturgical calendar using Romcal',
    endpoints: [
      '/health',
      '/today',
      '/date/:date',
      '/year/:year',
      '/season/:season/:year',
      '/info'
    ]
  });
});

// Today's liturgical day
app.get('/today', async (req, res) => {
  try {
    const today = new Date();
    const year = today.getFullYear();
    const romcal = new Romcal({ year });
    const calendar = await romcal.generateCalendar();
    
    const dateStr = today.toISOString().split('T')[0];
    const dayData = calendar.find(d => {
      const dDate = d.moment ? d.moment.toISOString().split('T')[0] : d.date;
      return dDate === dateStr;
    });
    
    if (!dayData) {
      return res.status(404).json({ error: 'Date not found' });
    }
    
    res.json(formatDay(dayData));
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get specific date (YYYY-MM-DD)
app.get('/date/:date', async (req, res) => {
  try {
    const dateStr = req.params.date;
    const year = parseInt(dateStr.split('-')[0]);
    
    if (isNaN(year) || year < 1970 || year > 2100) {
      return res.status(400).json({ error: 'Invalid year' });
    }
    
    const romcal = new Romcal({ year });
    const calendar = await romcal.generateCalendar();
    
    const dayData = calendar.find(d => {
      const dDate = d.moment ? d.moment.toISOString().split('T')[0] : 
                    (typeof d.date === 'object' ? d.date.toISOString().split('T')[0] : d.date);
      return dDate === dateStr;
    });
    
    if (!dayData) {
      return res.status(404).json({ error: `Date ${dateStr} not found` });
    }
    
    res.json(formatDay(dayData));
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get full year
app.get('/year/:year', async (req, res) => {
  try {
    const year = parseInt(req.params.year);
    
    if (isNaN(year) || year < 1970 || year > 2100) {
      return res.status(400).json({ error: 'Invalid year' });
    }
    
    const romcal = new Romcal({ year });
    const calendar = await romcal.generateCalendar();
    
    res.json({
      year: year,
      days: calendar.map(formatDay)
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get season
app.get('/season/:season/:year', async (req, res) => {
  try {
    const year = parseInt(req.params.year);
    const season = req.params.season.toLowerCase();
    
    if (isNaN(year) || year < 1970 || year > 2100) {
      return res.status(400).json({ error: 'Invalid year' });
    }
    
    const romcal = new Romcal({ year });
    const calendar = await romcal.generateCalendar();
    
    const seasonDays = calendar.filter(d => {
      const daySeason = (d.data?.season?.value || d.season || '').toLowerCase();
      return daySeason.includes(season);
    });
    
    res.json({
      season: req.params.season,
      year: year,
      days: seasonDays.map(formatDay)
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Format romcal output to match tempus-bede API
function formatDay(day) {
  const dateStr = day.moment ? day.moment.toISOString().split('T')[0] :
                  (typeof day.date === 'object' ? day.date.toISOString().split('T')[0] : day.date);
  
  return {
    date: dateStr,
    id: day.key || day.name?.toLowerCase().replace(/\s+/g, '-') || 'weekday',
    name: day.name || 'Weekday',
    rank: day.rank?.name || day.type || 'FERIA',
    season: day.data?.season?.value || day.season || 'Ordinary Time',
    color: [day.data?.meta?.liturgicalColor?.value || day.color || 'green'],
    isFeast: day.type === 'FEAST' || day.rank?.name === 'FEAST',
    isSolemnity: day.rank?.name === 'SOLEMNITY',
    isOptional: day.rank?.name === 'OPT_MEMORIAL',
    meta: {
      cycle: day.cycle?.value || day.data?.meta?.cycle?.value || 'A',
      weekday: new Date(dateStr).toLocaleDateString('en-US', { weekday: 'long' }),
      titles: day.data?.meta?.titles || []
    }
  };
}

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Bede service running on port ${PORT}`);
});
