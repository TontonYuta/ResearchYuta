#!/usr/bin/env python3
"""
Record Lesson Learned & Evolution Ledger
Appends new reflection entries into memory/evolution_ledger.jsonl
"""

import os
import sys
import json
import time
import argparse
from typing import Dict, Any

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
LEDGER_PATH = os.path.join(SKILL_ROOT, "memory", "evolution_ledger.jsonl")

CATEGORIES = [
    "TOOLING",
    "COMMUNICATION",
    "ARCHITECTURE",
    "TESTING",
    "USER_PREFERENCE",
    "CONTEXT_MANAGEMENT"
]

def record_lesson(
    category: str,
    trigger: str,
    mistake: str,
    lesson: str,
    rule: str = "",
    severity: str = "MEDIUM"
) -> Dict[str, Any]:
    os.makedirs(os.path.dirname(LEDGER_PATH), exist_ok=True)
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry_id = f"EVO-{int(time.time())}"
    
    entry = {
        "id": entry_id,
        "timestamp": timestamp,
        "category": category.upper(),
        "severity": severity.upper(),
        "trigger": trigger.strip(),
        "mistake": mistake.strip(),
        "lesson": lesson.strip(),
        "rule": rule.strip() if rule else lesson.strip()
    }
    
    with open(LEDGER_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        
    return entry

def main():
    parser = argparse.ArgumentParser(description="Record a lesson learned into the evolution ledger.")
    parser.add_argument("--category", choices=CATEGORIES, default="TOOLING", help="Category of the lesson")
    parser.add_argument("--trigger", required=True, help="What triggered this reflection (e.g. User comment, test fail)")
    parser.add_argument("--mistake", required=True, help="What was done incorrectly or inefficiently")
    parser.add_argument("--lesson", required=True, help="The insight or heuristic gained")
    parser.add_argument("--rule", default="", help="Actionable rule derived from this lesson")
    parser.add_argument("--severity", choices=["LOW", "MEDIUM", "HIGH", "CRITICAL"], default="MEDIUM", help="Severity level")
    
    args = parser.parse_args()
    
    entry = record_lesson(
        category=args.category,
        trigger=args.trigger,
        mistake=args.mistake,
        lesson=args.lesson,
        rule=args.rule,
        severity=args.severity
    )
    
    print("=" * 60)
    print(f"🧠 [Lesson Inscribed] {entry['id']} ({entry['timestamp']})")
    print(f"📂 Category: {entry['category']} | Severity: {entry['severity']}")
    print(f"🎯 Trigger:  {entry['trigger']}")
    print(f"⚠️  Mistake:  {entry['mistake']}")
    print(f"💡 Lesson:   {entry['lesson']}")
    print(f"📜 Rule:     {entry['rule']}")
    print(f"💾 Saved to: {LEDGER_PATH}")
    print("=" * 60)

if __name__ == "__main__":
    main()
