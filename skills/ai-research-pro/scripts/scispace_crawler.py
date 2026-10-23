#!/usr/bin/env python3
"""
SciSpace Literature Crawler & AI Research Extractor via Playwright
Integrates https://scispace.com/ with Playwright for AI-Assisted Research.
Features:
- Anti-WAF stealth browser configuration
- Persistent session management (--login, --status)
- Deep literature review extraction (papers, citations, TLDR, insights, synthesis)
- Markdown matrix and JSON dataset generation
"""

import os
import sys
import json
import base64
import time
import argparse
import asyncio
from typing import List, Dict, Any, Optional
from playwright.async_api import async_playwright, Page, BrowserContext

DEFAULT_SESSION_PATH = os.path.expanduser("~/.config/scispace_session.json")
SCISPACE_URL = "https://scispace.com"

def get_stealth_args():
    return [
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
        "--disable-infobars",
        "--disable-dev-shm-usage",
        "--disable-extensions",
    ]

async def apply_stealth(context: BrowserContext):
    await context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        window.chrome = {
            runtime: {}
        };
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en', 'vi']
        });
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });
    """)

def check_token_payload(token_str: str) -> Optional[Dict[str, Any]]:
    try:
        parts = token_str.split(".")
        if len(parts) >= 2:
            pad = len(parts[1]) % 4
            b64_str = parts[1] + ("=" * (4 - pad) if pad else "")
            payload = json.loads(base64.urlsafe_b64decode(b64_str).decode("utf-8"))
            return payload
    except Exception:
        pass
    return None

def check_session_status(session_path: str = DEFAULT_SESSION_PATH) -> Dict[str, Any]:
    if not os.path.exists(session_path):
        return {"valid": False, "reason": "No session file found"}
    try:
        with open(session_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        cookies = data.get("cookies", [])
        access_cookie = next((c for c in cookies if c.get("name") == "__Host-access"), None)
        if not access_cookie:
            return {"valid": False, "reason": "__Host-access cookie missing"}
        
        payload = check_token_payload(access_cookie.get("value", ""))
        if not payload:
            return {"valid": False, "reason": "Could not parse JWT in __Host-access"}
        
        exp = payload.get("exp", 0)
        user_type = payload.get("user_type", "UNKNOWN")
        is_guest = user_type == "GUEST"
        is_expired = time.time() > exp
        
        return {
            "valid": not is_expired and not is_guest,
            "user_type": user_type,
            "expired": is_expired,
            "expires_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(exp)) if exp else "Unknown",
            "sub": payload.get("sub"),
            "is_guest": is_guest
        }
    except Exception as e:
        return {"valid": False, "reason": str(e)}

async def interactive_login(session_path: str = DEFAULT_SESSION_PATH):
    print("=" * 65)
    print("🔑 SciSpace Interactive Login via Playwright")
    print(f"Session will be saved to: {session_path}")
    print("A browser window will open. Please log in with your Google or SciSpace account.")
    print("=" * 65)
    
    os.makedirs(os.path.dirname(session_path), exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=get_stealth_args()
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="en-US",
            timezone_id="Asia/Ho_Chi_Minh"
        )
        await apply_stealth(context)
        page = await context.new_page()
        
        print("\n[1/3] Navigating to https://scispace.com ...")
        await page.goto(SCISPACE_URL, wait_until="load", timeout=30000)
        
        # Click login button if present
        try:
            login_btn = page.locator("button:has-text('Login'), button:has-text('Sign in')").first
            if await login_btn.count() > 0:
                await login_btn.click()
        except Exception:
            pass
            
        print("[2/3] Waiting for user to complete login in the opened browser...")
        print("      (Watching for non-guest authentication token...)")
        
        authenticated = False
        start_time = time.time()
        timeout_seconds = 300  # 5 minutes
        
        while time.time() - start_time < timeout_seconds:
            cookies = await context.cookies()
            access_cookie = next((c for c in cookies if c.get("name") == "__Host-access"), None)
            if access_cookie:
                payload = check_token_payload(access_cookie.get("value", ""))
                if payload and payload.get("user_type") != "GUEST":
                    print(f"\n🎉 Login detected! User Type: {payload.get('user_type')}, Subject: {payload.get('sub')}")
                    authenticated = True
                    break
            await asyncio.sleep(2)
            
        if authenticated:
            await context.storage_state(path=session_path)
            print(f"[3/3] ✅ Successfully saved authentication session to:\n      {session_path}")
        else:
            print("\n❌ Login timed out or was not completed. Session not saved.")
            
        await browser.close()
        return authenticated

async def crawl_scispace_literature(
    query: str,
    max_papers: int = 10,
    session_path: str = DEFAULT_SESSION_PATH,
    headless: bool = True
) -> Dict[str, Any]:
    """
    Crawls SciSpace Literature Review for a query and extracts structured insights.
    """
    status = check_session_status(session_path)
    use_session = status.get("valid", False)
    
    if not use_session:
        print(f"⚠️ Notice: Valid SciSpace user session not found ({status.get('reason', 'Guest limit')}).")
        print("   Running in guest/public mode. For full unthrottled AI Insights, run:")
        print("   python scispace_crawler.py --login")
    else:
        print(f"🔒 Authenticated as SciSpace user (Type: {status.get('user_type')}).")

    extracted_data = {
        "query": query,
        "scispace_url": f"{SCISPACE_URL}/search?q={query.replace(' ', '+')}",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ai_synthesis": "",
        "papers": []
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless, args=get_stealth_args())
        
        context_kwargs = {
            "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "viewport": {"width": 1920, "height": 1080},
            "locale": "en-US",
            "timezone_id": "Asia/Ho_Chi_Minh"
        }
        if use_session and os.path.exists(session_path):
            context_kwargs["storage_state"] = session_path
            
        context = await browser.new_context(**context_kwargs)
        await apply_stealth(context)
        page = await context.new_page()

        search_url = f"{SCISPACE_URL}/search?q={query.replace(' ', '+')}"
        print(f"[SciSpace] Navigating to search: {search_url}")

        try:
            # First visit home to ensure AWS WAF cookies are fresh
            await page.goto(SCISPACE_URL, wait_until="load", timeout=20000)
            await page.wait_for_timeout(1500)
            
            await page.goto(search_url, wait_until="load", timeout=30000)
            await page.wait_for_timeout(4000)

            # Check if signup modal appeared and close it if possible
            try:
                close_btn = page.locator("button[aria-label*='close' i], button:has-text('✕')").first
                if await close_btn.count() > 0 and await close_btn.is_visible():
                    await close_btn.click()
                    await page.wait_for_timeout(1000)
                else:
                    await page.keyboard.press("Escape")
            except Exception:
                pass

            # Wait for content or table to populate
            await page.wait_for_timeout(3000)

            # 1. Extract Top AI Synthesis (Insights summary) if available
            synthesis_selectors = [
                "[data-testid='insights-summary']",
                ".insights-summary",
                "div:has-text('Insights from top papers') + div",
                ".summary-text",
            ]
            for sel in synthesis_selectors:
                el = page.locator(sel).first
                if await el.count() > 0 and await el.is_visible():
                    txt = (await el.inner_text()).strip()
                    if len(txt) > 30:
                        extracted_data["ai_synthesis"] = txt
                        print(f"[SciSpace] Captured AI Synthesis ({len(txt)} chars).")
                        break

            # 2. Extract Papers list
            # SciSpace lists papers either as table rows or article cards with links containing /papers/
            paper_links = await page.locator("a[href*='/papers/']").all()
            seen_urls = set()
            
            for link_el in paper_links:
                if len(extracted_data["papers"]) >= max_papers:
                    break
                
                href = await link_el.get_attribute("href") or ""
                if not href or href == "/papers/browse" or href in seen_urls:
                    continue
                seen_urls.add(href)

                full_url = href if href.startswith("http") else f"{SCISPACE_URL}{href}"
                title = (await link_el.inner_text()).strip()
                if not title or len(title) < 5 or title.lower() == "browse papers":
                    continue

                # Locate the parent container / card to get authors, date, citations, TLDR
                parent = link_el.locator("xpath=ancestor::tr | xpath=ancestor::div[contains(@class, 'card') or contains(@class, 'paper') or contains(@class, 'row')]").first
                
                authors = ""
                year = ""
                citations = ""
                tldr = ""
                doi = ""
                pdf_url = ""

                if await parent.count() > 0:
                    parent_text = await parent.inner_text()
                    lines = [line.strip() for line in parent_text.split("\n") if line.strip()]
                    
                    # Try to extract year and citations
                    for line in lines:
                        if "citations" in line.lower():
                            citations = line
                        if ("202" in line or "201" in line) and len(line) <= 30:
                            year = line
                        if "tldr:" in line.lower() or "summary:" in line.lower():
                            tldr = line
                    
                    pdf_btn = parent.locator("a[href*='.pdf'], a[href*='arxiv.org/pdf'], a[title*='PDF' i]").first
                    if await pdf_btn.count() > 0:
                        pdf_url = await pdf_btn.get_attribute("href") or ""

                extracted_data["papers"].append({
                    "title": title,
                    "scispace_url": full_url,
                    "authors": authors,
                    "year": year,
                    "citations": citations,
                    "tldr": tldr,
                    "pdf_url": pdf_url,
                    "doi": doi
                })

            print(f"[SciSpace] Extracted {len(extracted_data['papers'])} research papers.")

        except Exception as e:
            print(f"[SciSpace Error] {e}", file=sys.stderr)
        finally:
            await browser.close()

    return extracted_data

def format_markdown_report(data: Dict[str, Any]) -> str:
    md = []
    md.append(f"# Báo Cáo Tổng Hợp SciSpace: {data.get('query', '')}\n")
    md.append(f"- **Nguồn dữ liệu**: SciSpace Literature Review ({data.get('scispace_url')})")
    md.append(f"- **Thời gian quét**: {data.get('timestamp')}")
    md.append(f"- **Số lượng bài báo thu thập**: {len(data.get('papers', []))}\n")
    
    if data.get("ai_synthesis"):
        md.append("## 💡 Tổng Quan AI (Cross-Paper Synthesis)\n")
        md.append(f"> {data['ai_synthesis']}\n")
        
    md.append("## 📚 Ma Trận Bài Báo Khoa Học (SciSpace Matrix)\n")
    md.append("| STT | Tên bài báo | Năm / Trích dẫn | Liên kết SciSpace | Tóm tắt / TLDR |")
    md.append("| :--- | :--- | :--- | :--- | :--- |")
    
    for i, p in enumerate(data.get("papers", []), 1):
        clean_title = p['title'].replace('|', '-')
        year_cite = f"{p['year']} | {p['citations']}".strip(" |")
        link = f"[Xem trên SciSpace]({p['scispace_url']})"
        tldr = p['tldr'].replace('|', '-').replace('\n', ' ')[:150]
        md.append(f"| {i} | **{clean_title}** | {year_cite} | {link} | {tldr} |")
        
    return "\n".join(md)

def main():
    parser = argparse.ArgumentParser(description="SciSpace Literature Review Automation with Playwright")
    parser.add_argument("--query", "-q", help="Research topic or search query")
    parser.add_argument("--login", action="store_true", help="Launch interactive browser to log in and save session")
    parser.add_argument("--status", action="store_true", help="Check SciSpace session authentication status")
    parser.add_argument("--session", default=DEFAULT_SESSION_PATH, help="Path to session JSON file")
    parser.add_argument("--max-papers", type=int, default=10, help="Maximum number of papers to extract")
    parser.add_argument("--output", "-o", help="Path to output JSON file")
    parser.add_argument("--export-md", help="Path to output Markdown file")
    parser.add_argument("--headless", action="store_true", default=True, help="Run headless mode (default True)")
    parser.add_argument("--no-headless", action="store_false", dest="headless", help="Run with visible browser GUI")
    
    args = parser.parse_args()

    if args.status:
        st = check_session_status(args.session)
        print("🔍 SciSpace Session Status:")
        print(json.dumps(st, indent=2))
        sys.exit(0 if st.get("valid") else 1)

    if args.login:
        asyncio.run(interactive_login(args.session))
        sys.exit(0)

    if not args.query:
        parser.print_help()
        print("\n❌ Error: Please provide --query, --login, or --status.")
        sys.exit(1)

    results = asyncio.run(crawl_scispace_literature(
        query=args.query,
        max_papers=args.max_papers,
        session_path=args.session,
        headless=args.headless
    ))

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"📁 JSON dataset saved to: {args.output}")

    if args.export_md:
        os.makedirs(os.path.dirname(os.path.abspath(args.export_md)), exist_ok=True)
        md_text = format_markdown_report(results)
        with open(args.export_md, "w", encoding="utf-8") as f:
            f.write(md_text)
        print(f"📄 Markdown matrix saved to: {args.export_md}")

    # Summary
    print(f"\n✨ Extracted {len(results.get('papers', []))} papers for query: '{args.query}'")

if __name__ == "__main__":
    main()
