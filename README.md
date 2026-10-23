# Kho Kỹ Năng Nghiên Cứu Tự Động (AI Research Skills Hub)

Kho lưu trữ và phát triển các bộ kỹ năng chuyên biệt (**Skills**) phục vụ nghiên cứu khoa học, tổng quan y văn tự động và biên dịch học thuật bằng AI cho Google Antigravity & AI Agents.

---

## 📂 Cấu Trúc Kho Kỹ Năng

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
├── README.md                                         # Tài liệu chỉ mục
├── AGENTS.md                                         # Quy chuẩn Agent
└── GEMINI.md                                         # Quy chuẩn hệ thống AI
```

---

## ⚡ Cài Đặt Kỹ Năng Vào Hệ Thống

Chạy lệnh cài đặt để tự động kích hoạt kỹ năng `ai-research-pro` cho Antigravity và Gemini CLI:

```bash
cd /home/tontonyuta/Documents/Research
./install.sh
```

Lệnh này sẽ tự động symlink `skills/ai-research-pro` vào thư mục cấu hình toàn cục `~/.gemini/config/skills/ai-research-pro`. Bất kỳ thay đổi hoặc nâng cấp script nào trong repo này sẽ lập tức có hiệu lực ngay trong phiên làm việc của AI.

---

## 🛠️ Bộ Công Cụ Dòng Lệnh

| Kịch bản | Công dụng | Công nghệ |
| :--- | :--- | :--- |
| [`academic_crawler.py`](./skills/ai-research-pro/scripts/academic_crawler.py) | Tìm kiếm & trích xuất bài báo từ arXiv | Official arXiv REST API (Atom XML), tốc độ < 2s |
| [`scispace_crawler.py`](./skills/ai-research-pro/scripts/scispace_crawler.py) | Khai thác tổng quan tri thức chéo & trích dẫn | Playwright Chromium (Stealth Anti-WAF) |
| [`run_research.py`](./skills/ai-research-pro/scripts/run_research.py) | Pipeline nghiên cứu toàn diện đa nguồn | CLI Runner, tự động khử trùng lặp & xuất hồ sơ |
| [`compile_latex.sh`](./skills/ai-research-pro/scripts/compile_latex.sh) | Biên dịch tài liệu LaTeX tiếng Việt | `pdflatex` 2-pass + tự động dọn sạch rác trung gian |
