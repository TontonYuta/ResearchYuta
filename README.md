# Kho Kỹ Năng Nghiên Cứu & Tự Học Tự Động (AI Research & Self-Learning Skills Hub)

Kho lưu trữ và phát triển các bộ kỹ năng chuyên biệt (**Skills**) phục vụ nghiên cứu khoa học, tổng quan y văn tự động và cơ chế tự học phản tư (Reflexion) cho Google Antigravity & AI Agents.

---

## 📂 Danh Mục Các Kỹ Năng (Skills)

```
/home/tontonyuta/Documents/Research/
├── skills/
│   ├── ai-research-pro/                              # 1. Kỹ năng nghiên cứu khoa học chuyên sâu
│   │   ├── SKILL.md                                  # Cẩm nang nghiên cứu, cào dữ liệu & LaTeX
│   │   ├── scripts/                                  # Bộ công cụ: academic_crawler, scispace, run_research, latex
│   │   └── references/                               # Từ điển thuật ngữ & cẩm nang sư phạm AI
│   │
│   └── agent-continuous-learning/                    # 2. Kỹ năng tự học & tự tiến hóa liên tục (Reflexion)
│       ├── SKILL.md                                  # Cẩm nang tự phản tư, học từ lỗi & phản hồi user
│       ├── scripts/                                  # record_lesson.py, audit_memory.py
│       ├── references/                               # reflexion_protocol.md, anti_patterns.md
│       └── memory/                                   # evolution_ledger.jsonl (Sổ bộ nhớ dài hạn)
│
├── install.sh                                        # Script 1-click symlink skills vào ~/.gemini/config/skills/
├── .gitignore                                        # Loại trừ file rác, cache, build artifacts
├── README.md                                         # Tài liệu chỉ mục
├── AGENTS.md                                         # Quy chuẩn Agent
└── GEMINI.md                                         # Quy chuẩn hệ thống AI
```

---

## ⚡ Cài Đặt Kỹ Năng Vào Hệ Thống

Chạy lệnh cài đặt để tự động kích hoạt cả 2 kỹ năng cho Antigravity và Gemini CLI:

```bash
cd /home/tontonyuta/Documents/Research
./install.sh
```

Lệnh này sẽ tự động symlink các thư mục trong `skills/*` vào thư mục cấu hình toàn cục `~/.gemini/config/skills/`. Bất kỳ cải tiến mã nguồn hay cập nhật quy tắc nào trong kho này sẽ lập tức có hiệu lực tức thì trên toàn hệ thống.

---

## 🧠 Chi Tiết Về Kỹ Năng Tự Học (Agent Continuous Learning)

Kỹ năng [`agent-continuous-learning`](./skills/agent-continuous-learning/SKILL.md) hoạt động theo chu trình 4 bước:
1. **Bắt tín hiệu (Signal Detection)**: Nhận diện phản hồi chỉ trích, sửa sai từ người dùng hoặc lỗi từ test suite.
2. **Tự phẫu thuật gốc rễ (Root-Cause Post-Mortem)**: Phân tích nguyên nhân điểm mù nhận thức (giả định sai, lạm dụng công cụ nặng, thiếu kiểm tra).
3. **Chưng cất tri thức (Knowledge Distillation)**: Chuyển hóa kinh nghiệm thành quy tắc vàng (Golden Rule) hoặc điều cấm kỵ (Anti-pattern).
4. **Ghi vào bộ nhớ dài hạn (Memory Inscription)**: Tự động lưu vào `evolution_ledger.jsonl` và đề xuất cập nhật vào `AGENTS.md`.

* **Ghi bài học mới**:
  ```bash
  python3 skills/agent-continuous-learning/scripts/record_lesson.py \
    --category "TOOLING" \
    --trigger "User phản ánh X" \
    --mistake "Đã làm Y sai" \
    --lesson "Cần làm Z" \
    --rule "Quy tắc áp dụng từ nay về sau"
  ```
* **Kiểm toán bộ nhớ**:
  ```bash
  python3 skills/agent-continuous-learning/scripts/audit_memory.py
  ```
