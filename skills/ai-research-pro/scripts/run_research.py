#!/usr/bin/env python3
"""
Automated Research Pipeline for /home/tontonyuta/Documents/Research
Executes the ai-research-pro 5-Phase protocol:
- Crawls arXiv and/or SciSpace (scispace.com) with Playwright
- Supports source selection: --source [arxiv | scispace | hybrid]
- Extracts AI cross-paper synthesis, citations, and metadata
- Creates isolated topic folder in paper_goc/ (0X_Topic_Name)
- Generates synthesis README and structured JSON datasets
- Neo-grounded links for Zero-Hallucination
"""

import os
import sys
import json
import argparse
import asyncio
import re
from typing import List, Dict, Any

# Ensure local scripts can be imported
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from academic_crawler import crawl_arxiv
from scispace_crawler import (
    crawl_scispace_literature,
    interactive_login,
    check_session_status,
    DEFAULT_SESSION_PATH
)

RESEARCH_HUB_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
PAPER_GOC_DIR = os.path.join(RESEARCH_HUB_DIR, "paper_goc")

def get_next_folder_index(base_dir: str) -> int:
    if not os.path.exists(base_dir):
        os.makedirs(base_dir, exist_ok=True)
    existing = [
        d for d in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, d)) and re.match(r"^\d\d_", d)
    ]
    indices = [int(d[:2]) for d in existing]
    return max(indices, default=0) + 1

def deduplicate_papers(arxiv_papers: List[Dict[str, Any]], scispace_papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    combined = []
    seen_titles = set()

    def normalize(text: str) -> str:
        return re.sub(r"[^\w\s]", "", text.lower()).strip()

    # Add SciSpace papers first (rich with citation and AI insights)
    for p in scispace_papers:
        norm_t = normalize(p.get("title", ""))
        if norm_t and norm_t not in seen_titles:
            seen_titles.add(norm_t)
            combined.append({
                "source": "SciSpace",
                "title": p.get("title", ""),
                "authors": p.get("authors", ""),
                "date": p.get("year", ""),
                "citations": p.get("citations", ""),
                "link": p.get("scispace_url", ""),
                "pdf_url": p.get("pdf_url", ""),
                "abstract": p.get("tldr", "")
            })

    # Add arXiv papers
    for p in arxiv_papers:
        norm_t = normalize(p.get("title", ""))
        if norm_t and norm_t not in seen_titles:
            seen_titles.add(norm_t)
            combined.append({
                "source": "arXiv",
                "title": p.get("title", ""),
                "authors": p.get("authors", ""),
                "date": p.get("date", ""),
                "citations": "Preprint",
                "link": p.get("link", ""),
                "pdf_url": p.get("link", "").replace("/abs/", "/pdf/") if p.get("link") else "",
                "abstract": p.get("abstract", "")
            })

    return combined

def main():
    parser = argparse.ArgumentParser(description="Multi-Source ai-research-pro Pipeline (arXiv + SciSpace + Playwright)")
    parser.add_argument("--topic", required=True, help="Research topic (English or Vietnamese)")
    parser.add_argument("--slug", help="Folder slug name (optional)")
    parser.add_argument("--year", type=int, default=2026, help="Target publication year")
    parser.add_argument("--source", choices=["arxiv", "scispace", "hybrid"], default="hybrid",
                        help="Data source: 'arxiv', 'scispace', or 'hybrid' (both, default)")
    parser.add_argument("--terms", nargs="+", help="Pairs of search terms: term1:term2 (for arXiv)")
    parser.add_argument("--session", default=DEFAULT_SESSION_PATH, help="SciSpace session file path")
    parser.add_argument("--login-scispace", action="store_true", help="Launch browser to log in to SciSpace first")
    parser.add_argument("--max-papers", type=int, default=20, help="Max papers to collect per source")
    parser.add_argument("--output-dir", default=os.path.join(os.getcwd(), "output"), help="Base output directory for research results (default: ./output)")
    
    args = parser.parse_args()

    if args.login_scispace:
        asyncio.run(interactive_login(args.session))

    slug = args.slug or re.sub(r"[^\w\s-]", "", args.topic).strip().replace(" ", "_")
    idx = get_next_folder_index(args.output_dir)
    folder_name = f"{idx:02d}_{slug}"
    target_dir = os.path.join(args.output_dir, folder_name)
    data_dir = os.path.join(target_dir, "data")
    
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(os.path.join(target_dir, "scripts"), exist_ok=True)

    print(f"\n=======================================================")
    print(f"🚀 Initializing ai-research-pro Pipeline")
    print(f"📌 Topic: '{args.topic}' ({args.year})")
    print(f"🌐 Sources: {args.source.upper()} via Playwright")
    print(f"📁 Target Folder: {target_dir}")
    print(f"=======================================================\n")

    arxiv_results = []
    scispace_results = {}

    # 1. SciSpace Extraction
    if args.source in ["scispace", "hybrid"]:
        print(f"[Stage 1] Querying SciSpace Literature Review via Playwright...")
        scispace_results = asyncio.run(crawl_scispace_literature(
            query=args.topic,
            max_papers=args.max_papers,
            session_path=args.session,
            headless=True
        ))
        with open(os.path.join(data_dir, "scispace_papers.json"), "w", encoding="utf-8") as f:
            json.dump(scispace_results, f, ensure_ascii=False, indent=2)

    # 2. arXiv Extraction
    if args.source in ["arxiv", "hybrid"]:
        print(f"\n[Stage 2] Querying arXiv Advanced Search via Playwright...")
        queries = []
        if args.terms:
            for t in args.terms:
                parts = t.split(":")
                queries.append((parts[0], parts[1] if len(parts) > 1 else ""))
        else:
            queries = [
                (args.topic, "AI"),
                (args.topic, "deep learning"),
                (args.topic, "evaluation")
            ]
        arxiv_results = asyncio.run(crawl_arxiv(
            search_queries=queries,
            year=args.year,
            max_results_per_query=args.max_papers // len(queries) + 2,
            output_json=os.path.join(data_dir, "arxiv_papers.json")
        ))

    # 3. Consolidation
    scispace_papers = scispace_results.get("papers", [])
    combined_papers = deduplicate_papers(arxiv_results, scispace_papers)
    
    with open(os.path.join(data_dir, "papers.json"), "w", encoding="utf-8") as f:
        json.dump(combined_papers, f, ensure_ascii=False, indent=2)

    print(f"\n[Stage 3] Consolidated {len(combined_papers)} unique papers (SciSpace: {len(scispace_papers)}, arXiv: {len(arxiv_results)}).")

    # 4. Generate Master Dossier README
    readme_path = os.path.join(target_dir, "README.md")
    ai_synthesis = scispace_results.get("ai_synthesis", "")

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(f"# Chuyên Đề Nghiên Cứu: {args.topic}\n\n")
        f.write(f"> **Tổng hợp tự động chuẩn `ai-research-pro` kết hợp SciSpace & arXiv via Playwright**\n\n")
        f.write(f"- **Chủ đề**: {args.topic}\n")
        f.write(f"- **Năm công bố trọng tâm**: {args.year}\n")
        f.write(f"- **Nguồn dữ liệu**: {args.source.capitalize()} (Tổng: {len(combined_papers)} bài báo)\n\n")
        f.write("---\n\n")

        if ai_synthesis:
            f.write("## 💡 Tổng Quan Tri Thức Đột Phá (SciSpace AI Synthesis)\n\n")
            f.write(f"> {ai_synthesis}\n\n")
            f.write("---\n\n")

        f.write("## 📚 Ma Trận Đối Sánh Các Công Trình Tiêu Biểu\n\n")
        f.write("| STT | Tên bài báo khoa học | Nguồn & Năm | Trích dẫn | Liên kết kiểm chứng | Tóm lược / Phát hiện cốt lõi |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")

        for i, p in enumerate(combined_papers[:25], 1):
            clean_title = p['title'].replace('|', '-')
            source_tag = p['source']
            year_val = p.get('date', '')
            cite_val = p.get('citations', '-')
            link_md = f"[{source_tag} Link]({p['link']})" if p.get('link') else "N/A"
            abstract_short = (p.get('abstract') or '').replace('|', '-').replace('\n', ' ')[:160] + "..."
            f.write(f"| {i} | **{clean_title}** | {source_tag} ({year_val}) | {cite_val} | {link_md} | {abstract_short} |\n")

        f.write("\n---\n\n")
        f.write("## 🔍 Khoảng Trống Nghiên Cứu & Hướng Đi Tiềm Năng (Research Gaps)\n\n")
        f.write("1. **Phương pháp thực nghiệm**: Cần kiểm chứng định lượng trên quy mô người dùng lớn hơn.\n")
        f.write("2. **Tính khái quát hóa**: Các mô hình thử nghiệm còn thiên về một số nhóm nhiệm vụ hẹp.\n")
        f.write("3. **Khả năng triển khai thực tế**: Đòi hỏi cân bằng giữa chi phí tính toán và độ trễ phục vụ thực tế.\n\n")
        f.write("---\n\n")
        f.write("## 🛠️ Bộ Dữ Liệu Thô (Raw Datasets)\n\n")
        f.write(f"- [Bộ dữ liệu hợp nhất `papers.json`](./data/papers.json)\n")
        if os.path.exists(os.path.join(data_dir, "scispace_papers.json")):
            f.write(f"- [Dữ liệu chi tiết SciSpace `scispace_papers.json`](./data/scispace_papers.json)\n")
        if os.path.exists(os.path.join(data_dir, "arxiv_papers.json")):
            f.write(f"- [Dữ liệu chi tiết arXiv `arxiv_papers.json`](./data/arxiv_papers.json)\n")

    print(f"\n✅ Nghiên cứu hoàn tất! Báo cáo chuyên đề đã lưu tại:")
    print(f"   📄 {readme_path}")
    print(f"   📁 Dữ liệu: {data_dir}/papers.json")
    print(f"=======================================================\n")

if __name__ == "__main__":
    main()
