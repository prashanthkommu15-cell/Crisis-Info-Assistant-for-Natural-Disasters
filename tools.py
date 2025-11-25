"""project.tools.tools

Safe, dependency-light tools for demo. Replace with production APIs as needed.
"""
import time, random
from typing import List, Dict, Optional
import requests
import feedparser

def web_search(query: str, max_results: int = 3, newsapi_key: Optional[str] = None) -> List[Dict]:
    results = []
    try:
        if newsapi_key:
            url = "https://newsapi.org/v2/everything"
            params = {"q": query, "pageSize": max_results, "apiKey": newsapi_key, "sortBy": "publishedAt", "language": "en"}
            r = requests.get(url, params=params, timeout=10)
            r.raise_for_status()
            data = r.json()
            for a in data.get("articles", [])[:max_results]:
                results.append({
                    "title": a.get("title"),
                    "snippet": a.get("description") or a.get("content") or "",
                    "url": a.get("url"),
                    "timestamp": a.get("publishedAt")
                })
            if results:
                return results
    except Exception:
        pass

    for i in range(max_results):
        results.append({
            "title": f"Mock news {i+1} about {query}",
            "snippet": f"This is a simulated news snippet for '{query}'.",
            "url": f"https://example.com/news/{query.replace(' ', '_')}/{i+1}",
            "timestamp": time.time() - random.randint(0, 3600)
        })
    return results

def rss_fetch(feed_urls: List[str]) -> List[Dict]:
    items = []
    for url in feed_urls:
        try:
            parsed = feedparser.parse(url)
            for entry in parsed.entries[:5]:
                items.append({
                    "source": url,
                    "title": entry.get("title"),
                    "content": (entry.get("summary") or entry.get("description") or "") if entry else "",
                    "url": entry.get("link"),
                    "timestamp": entry.get("published") or entry.get("updated") or time.time()
                })
        except Exception:
            continue
    return items

def geo_lookup(location_text: Optional[str]) -> Dict:
    if not location_text:
        return {"city": None, "region": None, "country": None, "normalized": None}
    parts = [p.strip() for p in location_text.split(',') if p.strip()]
    city = parts[0] if parts else None
    region = parts[1] if len(parts) > 1 else None
    country = parts[-1] if parts else None
    normalized = ', '.join(parts)
    return {"city": city, "region": region, "country": country, "normalized": normalized}

def summarize_text(texts: List[str], max_sentences: int = 3) -> str:
    joined = " ".join([t for t in texts if t])
    sents = []
    for part in joined.split('.'):
        p = part.strip()
        if p:
            sents.append(p)
    if not sents:
        return ""
    sel = sents[:max_sentences]
    return '. '.join(sel) + ('.' if sel else '')

def generate_safety_instructions(hazard_type: str, location: Dict, detail_level: str = 'simple') -> str:
    hazard = (hazard_type or "general").lower()
    templates = {
        "flood": [
            "If you are in a flood-prone area, move to higher ground immediately.",
            "Avoid walking or driving through floodwaters; six inches of moving water can knock you down.",
            "Follow evacuation orders from local authorities and keep a battery-powered radio available."
        ],
        "earthquake": [
            "Drop, Cover, and Hold On until the shaking stops.",
            "Stay away from windows and heavy objects that could fall.",
            "After the shaking stops, check for hazards and follow local instructions."
        ],
        "wildfire": [
            "If authorities issue an evacuation order, leave immediately and follow main roads.",
            "Keep windows and doors closed; use N95 masks if smoke is heavy.",
            "Prepare an emergency kit and keep your phone charged."
        ],
        "storm": [
            "Secure outdoor items and stay indoors away from windows.",
            "Follow local advisories about flooding and wind hazards.",
            "Prepare emergency supplies and a communication plan."
        ],
        "general": [
            "Seek official guidance from local emergency services.",
            "Prioritize personal safety; follow instructions from trusted authorities."
        ]
    }
    chosen = templates.get(hazard, templates["general"])
    if detail_level == "detailed":
        return "\n".join([f"- {s} (see local agency guidance)" for s in chosen])
    return "\n".join([f"- {s}" for s in chosen])
