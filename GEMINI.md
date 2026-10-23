# Quy Chuẩn Hoạt Động Kỹ Năng Nghiên Cứu & Tự Học Tại /home/tontonyuta/Documents/Research

Tài liệu này là quy tắc chuẩn hóa (**Workspace Rules**) áp dụng cho kho kỹ năng nghiên cứu khoa học và tự học liên tục tại `/home/tontonyuta/Documents/Research`.

---

## 1. Cấu Trúc Kho Kỹ Năng

```
/home/tontonyuta/Documents/Research/
├── skills/
│   ├── ai-research-pro/                              # Kỹ năng nghiên cứu khoa học chuyên sâu
│   └── agent-continuous-learning/                    # Kỹ năng tự học & tự tiến hóa liên tục (Reflexion)
│       ├── SKILL.md
│       ├── scripts/ (record_lesson.py, audit_memory.py)
│       ├── references/ (reflexion_protocol.md, anti_patterns.md)
│       └── memory/ (evolution_ledger.jsonl)
├── install.sh                                        # Script 1-click symlink skills vào ~/.gemini/config/skills/
├── .gitignore
├── README.md
├── AGENTS.md
└── GEMINI.md
```

---

## 2. Kích Hoạt Kỹ Năng

* **Nghiên cứu khoa học**: Tuân thủ [`skills/ai-research-pro/SKILL.md`](./skills/ai-research-pro/SKILL.md).
* **Tự học & Phản tư**: Tuân thủ [`skills/agent-continuous-learning/SKILL.md`](./skills/agent-continuous-learning/SKILL.md).

---

## 3. Tiêu Chuẩn Tự Học & Cải Tiến Liên Tục

1. **Phản hồi của Người Dùng là Tín Hiệu Tối Thượng**:
   * Khi người dùng chỉnh sửa, chê trách hoặc yêu cầu đổi hướng tiếp cận, Agent phải lập tức kích hoạt phản tư nhận thức (Reflexion).
   * Không xin lỗi sáo rỗng. Phân tích nguyên nhân gốc rễ và ghi lại bài học vào [`skills/agent-continuous-learning/memory/evolution_ledger.jsonl`](./skills/agent-continuous-learning/memory/evolution_ledger.jsonl).
2. **Ngăn chặn lỗi tái diễn (Zero-Repeat Policy)**:
   * Trước khi đưa ra quyết định kiến trúc hoặc công cụ, đối chiếu với danh mục Anti-patterns trong `skills/agent-continuous-learning/references/anti_patterns.md`.
