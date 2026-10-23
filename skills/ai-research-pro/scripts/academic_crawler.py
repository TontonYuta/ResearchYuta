#!/usr/bin/env python3
"""
Academic Literature Crawler & Extractor for AI-Assisted Research
Uses arXiv REST API (Atom XML) for high-speed, zero-headless data extraction,
with optional Playwright fallback.
"""

import asyncio
import json
import os
import sys
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from typing import List, Dict, Any

ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}

def query_arxiv_api(
    term1: str,
    term2: str = "",
    year: int = 2026,
    max_results: int = 30
) -> List[Dict[str, Any]]:
    """Query official arXiv API directly via HTTP GET without launching headless browser."""
    terms = []
    if term1:
        terms.append(f'all:"{term1}"')
    if term2:
        terms.append(f'all:"{term2}"')
    
    query_str = " AND ".join(terms) if terms else "all:AI"
    params = {
        "search_query": query_str,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    url = f"http://export.arxiv.org/api/query?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ResearchSkillsHub/2.0 (mailto:tontonyuta@local)"}
    )

    papers = []
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            content = resp.read()
            root = ET.fromstring(content)
            entries = root.findall("atom:entry", ATOM_NS)
            for entry in entries:
                id_el = entry.find("atom:id", ATOM_NS)
                title_el = entry.find("atom:title", ATOM_NS)
                summary_el = entry.find("atom:summary", ATOM_NS)
                published_el = entry.find("atom:published", ATOM_NS)
                authors = [
                    a.find("atom:name", ATOM_NS).text
                    for a in entry.findall("atom:author", ATOM_NS)
                    if a.find("atom:name", ATOM_NS) is not None
                ]

                link = id_el.text.strip() if id_el is not None else ""
                title = " ".join((title_el.text or "").split()) if title_el is not None else ""
                abstract = " ".join((summary_el.text or "").split()) if summary_el is not None else ""
                pub_date = published_el.text.strip() if published_el is not None else ""

                if link and title:
                    papers.append({
                        "title": title,
                        "authors": ", ".join(authors),
                        "date": pub_date[:10] if len(pub_date) >= 10 else pub_date,
                        "link": link,
                        "abstract": abstract
                    })
    except Exception as e:
        print(f"  [API Warning] Error querying '{query_str}': {e}", file=sys.stderr)

    return papers

async def crawl_arxiv(
    search_queries: List[tuple],
    year: int = 2026,
    max_results_per_query: int = 30,
    output_json: str = "research_papers.json"
) -> List[Dict[str, Any]]:
    papers = {}

    for term1, term2 in search_queries:
        print(f"[API Crawl] Query: '{term1}' AND '{term2}' ({year})...")
        results = query_arxiv_api(term1, term2, year=year, max_results=max_results_per_query)
        print(f"  -> Found {len(results)} items via arXiv API")
        for p in results:
            if p["link"] not in papers:
                papers[p["link"]] = p

    paper_list = list(papers.values())
    print(f"\n[Success] Crawled {len(paper_list)} unique academic papers.")

    if output_json:
        out_dir = os.path.dirname(output_json)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(paper_list, f, ensure_ascii=False, indent=2)
        print(f"[Export] Saved dataset to {output_json}")

    return paper_list

if __name__ == "__main__":
    queries = [
        ("AI research agent", "scientific discovery"),
        ("deep research", "literature review"),
        ("autonomous research", "large language models")
    ]
    asyncio.run(crawl_arxiv(queries, year=2026, max_results_per_query=10))
