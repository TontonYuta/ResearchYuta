#!/usr/bin/env python3
"""
Academic Paper Translator & Terminology Explainer (English -> Vietnamese)
Implements the 3-Step Reflective Academic Translation Protocol:
1. Terminology Extraction
2. High-register Academic Translation with Dual-Term Tagging
3. Deep Conceptual Glossary & Pedagogical Notes
"""

import os
import sys
import json
import argparse

PROMPT_TEMPLATE = """
Bạn là một chuyên gia dịch thuật học thuật cao cấp và nhà nghiên cứu song ngữ Anh - Việt.
Nhiệm vụ của bạn là dịch đoạn trích bài báo khoa học sau sang tiếng Việt chuẩn xuất bản, đồng thời GIẢI NGHĨA SÂU BẢN CHẤT CÁC THUẬT NGỮ CHUYÊN NGÀNH.

VĂN BẢN TIẾNG ANH GỐC:
\"\"\"
{source_text}
\"\"\"

HÃY THỰC HIỆN THEO 3 BƯỚC NGHIÊM NGẶT SAU:

---
### PHẦN 1: BẢN DỊCH HỌC THUẬT CHUẨN XUẤT BẢN (ACADEMIC TRANSLATION)
- Dịch với văn phong học thuật, trang trọng, logic chặt chẽ.
- Áp dụng nguyên tắc "Định danh kép (Dual-Term Tagging)": Khi gặp thuật ngữ chuyên môn quan trọng lần đầu, hãy viết: [Thuật ngữ tiếng Việt] ([Thuật ngữ tiếng Anh gốc]).
- Giữ nguyên công thức toán ($...$), trích dẫn tác giả (Author et al., Year) và tên thuật toán.

---
### PHẦN 2: BẢNG GIẢI NGHĨA THUẬT NGỮ HỌC THUẬT CHUYÊN SÂU (CONCEPTUAL GLOSSARY)
Với mỗi thuật ngữ khoa học then chốt xuất hiện trong đoạn văn, hãy lập bảng đối sánh:

| Thuật ngữ gốc (EN) | Thuật ngữ chuẩn (VI) | Bản chất khái niệm & Ý nghĩa khoa học | Ngữ cảnh ứng dụng |
| :--- | :--- | :--- | :--- |
| [Ví dụ: Cognitive Offloading] | [Ủy thác nhận thức] | [Giải thích dễ hiểu bản chất hiện tượng: việc não bộ trao bớt gánh nặng tư duy/ghi nhớ cho công cụ ngoài...] | [Tâm lý học nhận thức, AI giáo dục] |

---
### PHẦN 3: GHI CHÚ DỊCH THUẬT & CẢNH BÁO HIỂU LẦM (TRANSLATOR'S CRITICAL NOTES)
- Chỉ ra 1–2 bẫy dịch thuật (False friends) hoặc sự khác biệt tinh tế giữa cách hiểu thông thường và định nghĩa chuẩn xác trong giới học thuật.
"""

def generate_translation_prompt(text: str) -> str:
    return PROMPT_TEMPLATE.format(source_text=text.strip())

def main():
    parser = argparse.ArgumentParser(description="Academic Translation & Terminology Explanation Pipeline")
    parser.add_argument("--input", help="Path to input text/markdown file")
    parser.add_argument("--output", help="Path to output markdown file")
    args = parser.parse_args()

    sample_text = (
        "Students increasingly study alongside generative artificial intelligence (AI), "
        "yet unguided access to fluent answers invites cognitive offloading, and there is little "
        "evidence on which configurations of AI tutoring produce learning. We demonstrate how "
        "introducing pedagogical friction through challenge-and-unlock mechanisms fosters "
        "self-regulated learning and preserves critical epistemic vigilance."
    )

    if args.input and os.path.exists(args.input):
        with open(args.input, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = sample_text
        print("[Info] No input file provided. Using sample academic excerpt.")

    prompt = generate_translation_prompt(content)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(prompt)
        print(f"✅ Generated translation prompt scaffold at: {args.output}")
    else:
        print("\n" + "="*50 + " GENERATED PROMPT " + "="*50)
        print(prompt)

if __name__ == "__main__":
    main()
