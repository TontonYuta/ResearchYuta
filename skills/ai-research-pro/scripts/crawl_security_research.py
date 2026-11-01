#!/usr/bin/env python3
"""
Playwright Grounded Crawler for Modern Cybersecurity (2026)
Crawls roadmap.sh, PortSwigger, GitHub repos, and fetches arXiv papers.
Strictly under 200 lines.
"""

import os
import sys
import json
import asyncio
import urllib.request
import xml.etree.ElementTree as ET
from playwright.async_api import async_playwright

OUTPUT_DIR = "/home/tontonyuta/ResearchYuta/paper_goc/01_Modern_Security_Zero_2026"
os.makedirs(OUTPUT_DIR, exist_ok=True)

TARGET_URLS = [
    {"name": "roadmap_sh_cybersecurity", "url": "https://roadmap.sh/cyber-security"},
    {"name": "tryhackme_paths", "url": "https://tryhackme.com/hacktivities"},
    {"name": "portswigger_academy", "url": "https://portswigger.net/web-security"},
    {"name": "github_awesome_security", "url": "https://github.com/sbilly/awesome-security"},
    {"name": "github_owasp_top10_llm", "url": "https://github.com/OWASP/www-project-top-10-for-large-language-model-applications"},
]

async def crawl_web_targets():
    results = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        for target in TARGET_URLS:
            name, url = target["name"], target["url"]
            print(f"[Playwright] Crawling {name} -> {url}...")
            page = await context.new_page()
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=25000)
                await asyncio.sleep(2)
                title = await page.title()
                
                # Extract text content
                text_content = await page.evaluate("""() => {
                    const article = document.querySelector('article') || document.querySelector('main') || document.body;
                    const links = Array.from(document.querySelectorAll('a'))
                        .map(a => ({ text: a.innerText.trim(), href: a.href }))
                        .filter(l => l.text.length > 3 && l.href.startsWith('http'))
                        .slice(0, 30);
                    return {
                        title: document.title,
                        headings: Array.from(document.querySelectorAll('h1, h2, h3')).map(h => h.innerText.trim()).filter(Boolean),
                        sample_text: article.innerText.slice(0, 3000),
                        links: links
                    };
                }""")
                results[name] = {"url": url, "title": title, "data": text_content}
                print(f"  ✅ Extracted {len(text_content.get('headings', []))} headings from {name}")
            except Exception as e:
                print(f"  ⚠️ Error crawling {name}: {e}")
                results[name] = {"url": url, "error": str(e)}
            finally:
                await page.close()
        await browser.close()
    return results

def fetch_arxiv_papers():
    query = 'cat:cs.CR AND ("cybersecurity education" OR "learning cybersecurity" OR "LLM security" OR "AI security")'
    encoded_q = urllib.parse.quote(query)
    url = f"http://export.arxiv.org/api/query?search_query={encoded_q}&start=0&max_results=8&sortBy=submittedDate&sortOrder=descending"
    print(f"[arXiv API] Fetching recent security papers...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ResearchYuta/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_data = resp.read()
        root = ET.fromstring(xml_data)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        papers = []
        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
            summary = entry.find("atom:summary", ns).text.strip().replace("\n", " ")
            published = entry.find("atom:published", ns).text.strip()
            pdf_link = ""
            for link in entry.findall("atom:link", ns):
                if link.attrib.get("title") == "pdf":
                    pdf_link = link.attrib.get("href")
            papers.append({
                "title": title,
                "summary": summary[:400] + "...",
                "published": published,
                "pdf_url": pdf_link
            })
        print(f"  ✅ Retrieved {len(papers)} papers from arXiv API.")
        return papers
    except Exception as e:
        print(f"  ⚠️ Error fetching arXiv: {e}")
        return []

def main():
    print("=== STARTING MODERN SECURITY 2026 GROUNDED RESEARCH ===")
    web_data = asyncio.run(crawl_web_targets())
    arxiv_data = fetch_arxiv_papers()
    
    combined = {
        "timestamp": "2026-11-02",
        "web_sources": web_data,
        "arxiv_papers": arxiv_data
    }
    
    output_file = os.path.join(OUTPUT_DIR, "crawled_security_grounding.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)
    print(f"\n🎉 Saved grounded research dataset to: {output_file}")

if __name__ == "__main__":
    main()
