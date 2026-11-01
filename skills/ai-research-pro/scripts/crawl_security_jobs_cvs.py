#!/usr/bin/env python3
"""
Playwright Crawler for Security Intern/Fresher/Middle CVs & JDs
Thu thập yêu cầu tuyển dụng và kỹ năng thực tế từ GitHub và các nguồn tuyển dụng.
Strictly under 200 lines.
"""

import os
import json
import asyncio
from playwright.async_api import async_playwright

OUTPUT_DIR = "/home/tontonyuta/ResearchYuta/paper_goc/01_Modern_Security_Zero_2026"
os.makedirs(OUTPUT_DIR, exist_ok=True)

TARGET_SOURCES = [
    {
        "name": "cybersecurity_resume_template",
        "url": "https://github.com/onursaritepe/CyberSecurity-Resume-Template"
    },
    {
        "name": "roadmap_cybersecurity_roles",
        "url": "https://roadmap.sh/cyber-security"
    },
    {
        "name": "awesome_soc_analyst",
        "url": "https://github.com/cyb3rs3c/Awesome-SOC-Analyst"
    },
    {
        "name": "owasp_web_security_testing_guide",
        "url": "https://github.com/OWASP/wstg"
    }
]

async def crawl_sources():
    results = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        
        for item in TARGET_SOURCES:
            name, url = item["name"], item["url"]
            print(f"[Playwright] Crawling {name} -> {url}...")
            page = await context.new_page()
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=25000)
                await asyncio.sleep(2)
                
                data = await page.evaluate("""() => {
                    const article = document.querySelector('article.markdown-body') || document.querySelector('main') || document.body;
                    const headers = Array.from(document.querySelectorAll('h1, h2, h3, h4'))
                        .map(h => h.innerText.trim()).filter(Boolean);
                    
                    const listItems = Array.from(document.querySelectorAll('li'))
                        .map(li => li.innerText.trim())
                        .filter(t => t.length > 15 && t.length < 200)
                        .slice(0, 35);
                    
                    return {
                        title: document.title,
                        headers: headers.slice(0, 20),
                        listItems: listItems,
                        textSnippet: article ? article.innerText.slice(0, 4000) : ""
                    };
                }""")
                results[name] = {"url": url, "data": data}
                print(f"  ✅ Extracted {len(data['listItems'])} skill/competency items from {name}")
            except Exception as e:
                print(f"  ⚠️ Error crawling {name}: {e}")
                results[name] = {"url": url, "error": str(e)}
            finally:
                await page.close()
                
        await browser.close()
    return results

def main():
    print("=== STARTING SECURITY CV & JD COMPETENCY CRAWLER ===")
    crawled_data = asyncio.run(crawl_sources())
    
    output_file = os.path.join(OUTPUT_DIR, "crawled_security_cv_jd.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(crawled_data, f, ensure_ascii=False, indent=2)
    print(f"\n🎉 Saved CV & JD research data to: {output_file}")

if __name__ == "__main__":
    main()
