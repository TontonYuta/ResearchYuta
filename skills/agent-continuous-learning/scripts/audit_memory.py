#!/usr/bin/env python3
"""
Audit Memory & Reflection Ledger
Analyzes accumulated lessons, identifies recurring patterns, and suggests workspace rules.
"""

import os
import sys
import json
import argparse
from collections import Counter
from typing import List, Dict, Any

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
LEDGER_PATH = os.path.join(SKILL_ROOT, "memory", "evolution_ledger.jsonl")

def load_entries() -> List[Dict[str, Any]]:
    if not os.path.exists(LEDGER_PATH):
        return []
    entries = []
    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except Exception:
                    continue
    return entries

def audit_summary():
    entries = load_entries()
    total = len(entries)
    
    print("=" * 65)
    print("🧠 AGENT CONTINUOUS LEARNING - MEMORY AUDIT REPORT")
    print(f"Ledger File: {LEDGER_PATH}")
    print(f"Total Lessons Recorded: {total}")
    print("=" * 65)
    
    if total == 0:
        print("\n[Notice] No lessons recorded yet. The memory ledger is clean.")
        return
        
    categories = Counter(e.get("category", "UNKNOWN") for e in entries)
    severities = Counter(e.get("severity", "MEDIUM") for e in entries)
    
    print("\n📊 Phân bổ theo Danh mục:")
    for cat, count in categories.most_common():
        pct = (count / total) * 100
        print(f"  • {cat:<20}: {count:>3} ({pct:5.1f}%)")
        
    print("\n🚨 Phân bổ theo Mức độ nghiêm trọng:")
    for sev, count in severities.most_common():
        pct = (count / total) * 100
        print(f"  • {sev:<20}: {count:>3} ({pct:5.1f}%)")
        
    print("\n📜 Danh Sách Quy Tắc Đã Đúc Kết (Golden Rules):")
    for i, e in enumerate(entries[-10:], 1):
        print(f"  {i}. [{e.get('category')}] {e.get('rule')}")
        print(f"     ↳ Nguyên nhân: {e.get('mistake')}")
        
    print("\n" + "=" * 65)

def export_markdown(output_file: str):
    entries = load_entries()
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Sổ Nhật Ký Tiến Hóa Của Agent (Agent Evolution Ledger)\n\n")
        f.write(f"> Tổng số bài học đã ghi nhận: **{len(entries)}**\n\n")
        f.write("| STT | Mã bài học | Thời gian | Danh mục | Mức độ | Quy tắc vàng / Bài học đúc kết |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for i, e in enumerate(entries, 1):
            rule_clean = e.get("rule", "").replace("|", "-")
            f.write(f"| {i} | `{e.get('id')}` | {e.get('timestamp')} | **{e.get('category')}** | `{e.get('severity')}` | {rule_clean} |\n")
    print(f"✅ Exported memory report to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Audit the agent's memory ledger.")
    parser.add_argument("--summary", action="store_true", default=True, help="Print summary report")
    parser.add_argument("--export", help="Export summary to a Markdown file")
    
    args = parser.parse_args()
    
    if args.export:
        export_markdown(args.export)
    else:
        audit_summary()

if __name__ == "__main__":
    main()
