# Quy Chuẩn Hoạt Động Kỹ Năng Nghiên Cứu Tại /home/tontonyuta/Documents/Research

Tài liệu này là quy tắc chuẩn hóa (**Workspace Rules**) áp dụng cho kho kỹ năng nghiên cứu khoa học tự động tại `/home/tontonyuta/Documents/Research`.

---

## 1. Cấu Trúc Kho Kỹ Năng Nghiên Cứu (Research Skills Hub)

Thư mục `/home/tontonyuta/Documents/Research/` được tinh gọn thành **Kho Kỹ Năng Nghiên Cứu Chuyên Biệt**:

```
/home/tontonyuta/Documents/Research/
├── skills/
│   └── ai-research-pro/                              # Kỹ năng nghiên cứu khoa học chuyên sâu
│       ├── SKILL.md                                  # Cẩm nang kỹ năng toàn diện duy nhất
│       ├── scripts/                                  # Bộ công cụ dòng lệnh tự động hóa:
│       │   ├── academic_crawler.py                   # Cào arXiv tốc độ cao qua REST API chính thức
│       │   ├── scispace_crawler.py                   # Cào SciSpace Literature Review via Playwright
│       │   ├── run_research.py                       # CLI tổng hợp đa nguồn (arXiv + SciSpace)
│       │   ├── academic_translator.py                # Phản tư dịch thuật học thuật 3 bước
│       │   └── compile_latex.sh                      # Trình biên dịch LaTeX & tự dọn rác build
│       └── references/                               # Từ điển thuật ngữ & cẩm nang sư phạm AI
│           ├── ai_pedagogy_master_guide.md
│           ├── anti_jargon_plain_language_dictionary.md
│           └── papers_and_repos.md
│
├── install.sh                                        # Script 1-click symlink skills vào ~/.gemini/config/skills/
├── .gitignore                                        # Loại trừ file rác, cache, build artifacts
├── README.md                                         # Hướng dẫn sử dụng kho kỹ năng
├── AGENTS.md                                         # Quy chuẩn cho Agent
└── GEMINI.md                                         # Quy chuẩn đồng bộ hệ thống AI
```

---

## 2. Kích Hoạt Kỹ Năng: `skills/ai-research-pro/SKILL.md`

Mọi tác vụ nghiên cứu, tìm kiếm tài liệu, cào dữ liệu, tổng quan học thuật hoặc dịch thuật tuân theo tài liệu:
* **Tệp kỹ năng chuẩn**: [`skills/ai-research-pro/SKILL.md`](./skills/ai-research-pro/SKILL.md)

---

## 3. Tiêu Chuẩn Thực Thi

1. **Thu thập dữ liệu nhanh & chính xác**:
   * Ưu tiên dùng arXiv Official REST API (`academic_crawler.py`) cho tốc độ tính bằng giây và không tốn tài nguyên.
   * Sử dụng Playwright Stealth (`scispace_crawler.py`) khi cần khai thác tính năng độc quyền của SciSpace (AI synthesis, trích dẫn, ma trận thuộc tính).
2. **Dịch thuật & Biên soạn LaTeX**:
   * Bình dân hóa ngôn ngữ, loại bỏ thuật ngữ sáo rỗng (Plain Language).
   * Tự động dọn dẹp các tệp tin tạm (`.aux`, `.log`, `.out`) sau khi biên dịch PDF thành công.
