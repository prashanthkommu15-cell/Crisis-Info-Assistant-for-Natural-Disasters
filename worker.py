from typing import Dict, List
from project.tools.tools import web_search, rss_fetch, geo_lookup, summarize_text, generate_safety_instructions
from project.core.a2a_protocol import make_worker_result
from project.core.observability import Logger

class Worker:
    def __init__(self, memory=None):
        self.memory = memory

    def execute(self, plan: Dict) -> Dict:
        Logger.log({'agent':'worker','event':'execute_start','plan':plan})
        location = plan.get('location')
        loc_info = geo_lookup(location) if location else {'normalized': location}

        feed_urls = []
        if plan.get('hazard') == 'earthquake':
            feed_urls = ['https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.atom']
        elif plan.get('hazard') == 'flood':
            feed_urls = []
        else:
            feed_urls = ['https://www.reuters.com/world/rss.xml']

        rss_hits = rss_fetch(feed_urls) if feed_urls else []
        query = f"{plan.get('hazard')} {loc_info.get('normalized') or ''}".strip()
        web_hits = web_search(query, max_results=3)

        raw_texts: List[str] = []
        for h in web_hits:
            raw_texts.append(h.get('snippet') or '')
        for r in rss_hits:
            raw_texts.append(r.get('content') or r.get('title') or '')

        summary = summarize_text(raw_texts, max_sentences=3)
        instructions = generate_safety_instructions(plan.get('hazard','general'), loc_info, detail_level=plan.get('detail_level','simple'))

        sources = []
        for h in web_hits:
            if h.get('url'):
                sources.append(h.get('url'))
        for r in rss_hits:
            if r.get('url'):
                sources.append(r.get('url'))
            else:
                sources.append(r.get('source'))

        confidence = 0.5
        if web_hits or rss_hits:
            confidence = 0.8

        result = make_worker_result(summary=summary, safety=instructions, sources=sources, confidence=confidence)
        Logger.log({'agent':'worker','event':'execute_complete','result_summary': summary[:200], 'confidence': confidence})
        return result
