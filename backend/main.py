"""beets-viz API - FastAPI backend for music library visualization"""
import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
import sqlite3
from typing import Optional
from datetime import datetime

app = FastAPI(title="beets-viz API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths - configured via env vars
BEETS_DB = Path(os.getenv("BEETS_DB", "/home/stephen/.beets/config/musiclibrary.blb"))
MUSIC_PATH = os.getenv("MUSIC_PATH", "/home/stephen/media/music/beets-lib")

def map_path(db_path):
    """Map beets DB paths to actual filesystem paths.
    
    Beets stores paths like /music/Artist/Album/...
    In Docker: /music is mounted, so paths work as-is
    On host: need to map /music -> actual MUSIC_PATH
    """
    if not db_path:
        return None
    # If path starts with /music and MUSIC_PATH is different, map it
    if db_path.startswith("/music") and MUSIC_PATH != "/music":
        return db_path.replace("/music", MUSIC_PATH, 1)
    return db_path

def get_db():
    conn = sqlite3.connect(BEETS_DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def root():
    return {"status": "ok", "service": "beets-viz"}

@app.get("/api/stats")
def get_stats():
    conn = get_db()
    c = conn.cursor()
    stats = {}
    
    c.execute("SELECT COUNT(*) FROM albums")
    stats["total_albums"] = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM items")
    stats["total_tracks"] = c.fetchone()[0]
    c.execute("SELECT COUNT(DISTINCT albumartist) FROM albums")
    stats["total_artists"] = c.fetchone()[0]
    c.execute("SELECT COUNT(DISTINCT genre) FROM albums WHERE genre IS NOT NULL AND genre != ''")
    stats["total_genres"] = c.fetchone()[0]
    c.execute("SELECT COUNT(DISTINCT label) FROM albums WHERE label IS NOT NULL AND label != ''")
    stats["total_labels"] = c.fetchone()[0]
    c.execute("SELECT SUM(length) FROM items")
    total_seconds = c.fetchone()[0] or 0
    stats["total_duration_hours"] = round(total_seconds / 3600, 1)
    c.execute("SELECT MIN(year), MAX(year) FROM albums WHERE year > 0 AND year < 2100")
    row = c.fetchone()
    stats["year_range"] = {"min": row[0], "max": row[1]}
    
    conn.close()
    return stats

@app.get("/api/albums")
def get_albums(
    limit: int = Query(50, le=500),
    offset: int = 0,
    sort: str = "added",
    order: str = "desc",
    genre: Optional[str] = None,
    label: Optional[str] = None,
    year: Optional[int] = None,
    search: Optional[str] = None,
):
    conn = get_db()
    c = conn.cursor()
    
    # Build WHERE clause
    where = "WHERE 1=1"
    params = []
    
    if genre:
        where += " AND genre LIKE ?"
        params.append(f"%{genre}%")
    if label:
        where += " AND label LIKE ?"
        params.append(f"%{label}%")
    if year:
        where += " AND year = ?"
        params.append(year)
    if search:
        where += " AND (albumartist LIKE ? OR album LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
    
    # Get total count first (same filters, no limit/offset)
    c.execute(f"SELECT COUNT(*) FROM albums {where}", params)
    total = c.fetchone()[0]
    
    # Now get paginated results
    query = f"SELECT id, albumartist, album, year, genre, label, artpath, added FROM albums {where}"
    sort_col = {"added": "added", "year": "year", "artist": "albumartist", "album": "album"}.get(sort, "added")
    query += f" ORDER BY {sort_col} {'DESC' if order == 'desc' else 'ASC'}"
    query += " LIMIT ? OFFSET ?"
    
    c.execute(query, params + [limit, offset])
    albums = []
    for row in c.fetchall():
        artpath = row["artpath"].decode() if row["artpath"] else None
        albums.append({
            "id": row["id"],
            "artist": row["albumartist"],
            "album": row["album"],
            "year": row["year"],
            "genre": row["genre"],
            "label": row["label"],
            "artpath": map_path(artpath),
            "added": row["added"],
        })
    
    conn.close()
    return {"albums": albums, "total": total, "limit": limit, "offset": offset}

@app.get("/api/timeline")
def get_timeline():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT year, COUNT(*) as count FROM albums 
        WHERE year > 0 AND year < 2100
        GROUP BY year ORDER BY year
    """)
    timeline = [{"year": row[0], "count": row[1]} for row in c.fetchall()]
    conn.close()
    return timeline

@app.get("/api/genres")
def get_genres():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT genre, COUNT(*) as count FROM albums 
        WHERE genre IS NOT NULL AND genre != ''
        GROUP BY genre ORDER BY count DESC
    """)
    
    genre_counts = {}
    for row in c.fetchall():
        genres = [g.strip() for g in row[0].split(',')]
        for genre in genres:
            if genre:
                genre_counts[genre] = genre_counts.get(genre, 0) + row[1]
    
    genres = [{"name": k, "count": v} for k, v in sorted(genre_counts.items(), key=lambda x: -x[1])]
    conn.close()
    return genres[:100]

@app.get("/api/labels")
def get_labels(limit: int = 50):
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT label, COUNT(*) as count FROM albums 
        WHERE label IS NOT NULL AND label != ''
        GROUP BY label ORDER BY count DESC LIMIT ?
    """, [limit])
    labels = [{"name": row[0], "count": row[1]} for row in c.fetchall()]
    conn.close()
    return labels

@app.get("/api/artists")
def get_artists(limit: int = 50):
    conn = get_db()
    c = conn.cursor()
    # Exclude compilation/various artist names
    c.execute("""
        SELECT albumartist, COUNT(*) as count FROM albums 
        WHERE LOWER(albumartist) NOT IN ('various artists', 'various', 'va', 'soundtrack', 'original soundtrack')
          AND albumartist IS NOT NULL AND albumartist != ''
        GROUP BY albumartist ORDER BY count DESC LIMIT ?
    """, [limit])
    artists = [{"name": row[0], "count": row[1]} for row in c.fetchall()]
    conn.close()
    return artists

@app.get("/api/recent")
def get_recent(limit: int = 20):
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT id, albumartist, album, year, genre, artpath, added
        FROM albums ORDER BY added DESC LIMIT ?
    """, [limit])
    
    albums = []
    for row in c.fetchall():
        artpath = row["artpath"].decode() if row["artpath"] else None
        albums.append({
            "id": row["id"],
            "artist": row["albumartist"],
            "album": row["album"],
            "year": row["year"],
            "genre": row["genre"],
            "artpath": map_path(artpath),
            "added": row["added"],
            "added_date": datetime.fromtimestamp(row["added"]).isoformat() if row["added"] else None,
        })
    conn.close()
    return albums

@app.get("/api/countries")
def get_countries():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT country, COUNT(*) as count FROM albums 
        WHERE country IS NOT NULL AND country != ''
        GROUP BY country ORDER BY count DESC
    """)
    countries = [{"code": row[0], "count": row[1]} for row in c.fetchall()]
    conn.close()
    return countries

@app.get("/api/decades")
def get_decades():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT (year / 10) * 10 as decade, COUNT(*) as count FROM albums 
        WHERE year > 0 AND year < 2100
        GROUP BY decade ORDER BY decade
    """)
    decades = [{"decade": row[0], "count": row[1]} for row in c.fetchall()]
    conn.close()
    return decades

@app.get("/api/artist/{name}")
def get_artist_albums(
    name: str,
    limit: int = Query(50, le=500),
    offset: int = 0,
    sort: str = "year",
    order: str = "asc",
):
    """Get albums for a specific artist with pagination"""
    conn = get_db()
    c = conn.cursor()
    
    # Get total count
    c.execute("SELECT COUNT(*) FROM albums WHERE albumartist = ?", [name])
    total = c.fetchone()[0]
    
    # Get paginated albums
    sort_col = {"added": "added", "year": "year", "album": "album"}.get(sort, "year")
    c.execute(f"""
        SELECT id, albumartist, album, year, genre, label, artpath, added 
        FROM albums WHERE albumartist = ?
        ORDER BY {sort_col} {'DESC' if order == 'desc' else 'ASC'}
        LIMIT ? OFFSET ?
    """, [name, limit, offset])
    
    albums = []
    for row in c.fetchall():
        artpath = row["artpath"].decode() if row["artpath"] else None
        albums.append({
            "id": row["id"],
            "artist": row["albumartist"],
            "album": row["album"],
            "year": row["year"],
            "genre": row["genre"],
            "label": row["label"],
            "artpath": map_path(artpath),
            "added": row["added"],
        })
    
    conn.close()
    return {"artist": name, "albums": albums, "total": total, "limit": limit, "offset": offset}

@app.get("/api/album/{album_id}")
def get_album(album_id: int):
    conn = get_db()
    c = conn.cursor()
    
    c.execute("SELECT * FROM albums WHERE id = ?", [album_id])
    row = c.fetchone()
    if not row:
        conn.close()
        return {"error": "Album not found"}
    
    album = dict(row)
    if album.get("artpath"):
        album["artpath"] = map_path(album["artpath"].decode())
    
    c.execute("""
        SELECT title, track, length, bitrate, format FROM items 
        WHERE album_id = ? ORDER BY disc, track
    """, [album_id])
    album["tracks"] = [dict(r) for r in c.fetchall()]
    
    conn.close()
    return album

@app.get("/api/art")
def get_album_art(path: str):
    """Serve album art with path validation to prevent traversal attacks."""
    art_path = Path(path).resolve()
    music_root = Path(MUSIC_PATH).resolve()
    
    # Security: ensure path is within music directory
    try:
        art_path.relative_to(music_root)
    except ValueError:
        return {"error": "Invalid path"}
    
    if not art_path.exists():
        return {"error": "Art not found"}
    
    # Only serve image files
    if art_path.suffix.lower() not in {'.jpg', '.jpeg', '.png', '.gif', '.webp'}:
        return {"error": "Invalid file type"}
    
    return FileResponse(art_path, media_type="image/jpeg")
