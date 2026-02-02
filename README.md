# beets-viz 🎵

A swank web UI for exploring your beets music library.

## Stack
- **Backend**: FastAPI (Python)
- **Frontend**: SvelteKit + Tailwind + D3.js
- **Data**: Beets SQLite database

## Features
- 📊 Collection dashboard & stats
- 📅 Release timeline visualization
- 🎨 Genre treemap explorer
- 🏷️ Label deep-dive
- 🖼️ Interactive album art wall
- 🗺️ Country map
- 🔗 Artist network graph

## Development

```bash
# Backend
cd backend && pip install -r requirements.txt && uvicorn main:app --reload

# Frontend
cd frontend && npm install && npm run dev
```

## Production

```bash
docker-compose up -d
```
