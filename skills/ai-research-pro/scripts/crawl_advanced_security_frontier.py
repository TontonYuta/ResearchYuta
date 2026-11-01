#!/usr/bin/env python3
"""
Playwright Grounded Crawler for Advanced Cybersecurity Frontiers (2026)
Crawls top-rated GitHub repositories and arXiv papers for:
1. Binary & Heap Exploitation (how2heap)
2. Kernel Exploitation & EDR Evasion (linux-kernel-exploitation, SysWhispers3)
3. Hardware Glitching & Fault Injection (ChipWhisperer)
4. Post-Quantum Cryptography (liboqs, NIST FIPS 203/204)
5. AI Adversarial Warfare & Agent Security
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

TARGET_REPOS = [
    {"name": "how2heap_glibc", "url": "https://github.com/shellphish/how2heap"},
    {"name": "linux_kernel_exploitation", "url": "https://github.com/xairy/linux-kernel-exploitation"},
    {"name": "syswhispers3_edr_evasion", "url": "https://github.com/klezVirus/SysWhispers3"},
    {"name": "chipwhisperer_hardware", "url": "https://github.com/newaetech/chipwhisperer"},
    {"name": "liboqs_post_quantum", "url": "https://github.com/open-quantum-safe/liboqs"},
    {"name": "awesome_adversarial_ml", "url": "https://github.com/yenchenlin/awesome-adversarial-machine-learning"}
]

ARXIV_QUERIES = [
    "all:post-quantum+cryptography+AND+all:fault+injection",
    "all:kernel+exploitation+AND+all:ebpf",
    "all:edr+evasion+AND+all:syscall",
    "all:prompt+injection+AND+all:agent"
]

async def crawl_github_repos():
    repo_results = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        for target in TARGET_REPOS:
            name, url = target["name"], target["url"]
            print(f"[Playwright] Crawling {name} -> {url}...")
            page = await context.new_page()
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await asyncio.sleep(2)
                title = await page.title()
                
                # Extract README, topics, and headings
                content = await page.evaluate("""() => {
                    const readme = document.querySelector('article') || document.querySelector('#readme') || document.body;
                    const headings = Array.from(readme.querySelectorAll('h1, h2, h3, h4'))
                        .map(h => h.innerText.trim()).filter(Boolean);
                    const listItems = Array.from(readme.querySelectorAll('li'))
                        .map(li => li.innerText.trim()).filter(t => t.length > 5).slice(0, 40);
                    return {
                        title: document.title,
                        headings: headings.slice(0, 25),
                        sample_bullets: listItems,
                        summary_text: readme.innerText.slice(0, 2500)
                    };
                }""")
                repo_results[name] = {"url": url, "title": title, "data": content}
                print(f"  ✅ Extracted {len(content.get('headings', []))} headings and {len(content.get('sample_bullets', []))} bullets from {name}")
            except Exception as e:
                print(f"  ⚠️ Error crawling {name}: {e}")
                repo_results[name] = {"url": url, "error": str(e)}
            finally:
                await page.close()
        await browser.close()
    return repo_results

def fetch_arxiv_papers():
    papers = []
    base_url = "http://export.arxiv.org/api/query?search_query="
    for q in ARXIV_QUERIES:
        url = f"{base_url}{q}&start=0&max_results=3&sortBy=submittedDate&sortOrder=descending"
        print(f"[ArXiv API] Fetching: {q}...")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'ResearchBot/2.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                xml_data = resp.read()
                root = ET.fromstring(xml_data)
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                for entry in root.findall('atom:entry', ns):
                    title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
                    summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
                    id_url = entry.find('atom:id', ns).text.strip()
                    published = entry.find('atom:published', ns).text.strip()
                    papers.append({
                        "query": q,
                        "title": title,
                        "url": id_url,
                        "published": published,
                        "summary": summary[:400] + "..."
                    })
        except Exception as e:
            print(f"  ⚠️ ArXiv error for {q}: {e}")
    return papers

async def main():
    print("=== STARTING ADVANCED SECURITY FRONTIER RESEARCH (2026) ===")
    repo_data = await crawl_github_repos()
    papers = fetch_arxiv_papers()
    
    final_output = {
        "timestamp": "2026-11-02",
        "grounding_method": "Playwright Headless Chromium + ArXiv API",
        "repositories": repo_data,
        "academic_papers": papers
    }
    
    out_file = os.path.join(OUTPUT_DIR, "advanced_security_frontier.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(final_output, f, ensure_ascii=False, indent=2)
    print(f"🎉 Research completed! Output saved to: {out_file}")

if __name__ == "__main__":
    asyncio.run(main())
