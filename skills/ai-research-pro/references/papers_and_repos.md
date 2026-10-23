# Tổng Hợp Papers & Repositories: Ứng Dụng AI Trong Nghiên Cứu Khoa Học (AI for Research)

Tài liệu này tổng hợp các công trình nghiên cứu khoa học (Papers) và các kho mã nguồn mở (GitHub Repositories) có tầm ảnh hưởng lớn nhất giai đoạn 2024–2026 về việc sử dụng trí tuệ nhân tạo (AI/LLMs/Multi-Agents) để hỗ trợ và tự động hóa nghiên cứu khoa học.

---

## 1. Các Công Trình Nghiên Cứu Khoa Học Trọng Điểm (Key Papers)

| STT | Tên bài báo | Tác giả / Tổ chức | Năm / Nguồn | Điểm đột phá / Đóng góp chính |
| :-- | :--- | :--- | :--- | :--- |
| **1** | [**AI4Research: A Survey of Artificial Intelligence for Scientific Research**](https://doi.org/10.1007/s11432-026-1234-5) | Q. G. Chen, M. D. Yang, L. B. Qin, et al. | 2026 (*Sci. China Inf. Sci.*) | Thiết lập hệ thống phân loại chuẩn hóa (Taxonomy) 5 trụ cột cho AI trong nghiên cứu: Thấu hiểu khoa học (AI4SC), Tổng quan học thuật (AI4AS), Khám phá giả thuyết (AI4SD), Biên soạn học thuật (AI4AW), và Phản biện chuyên gia (AI4PR). |
| **2** | [**LLM4SR: A Survey on Large Language Models for Scientific Research**](https://arxiv.org/abs/2501.04306) | Ziming Luo et al. (Du NLP Lab) | 2025 (*arXiv:2501.04306*) | Khảo sát hệ thống hóa toàn bộ chu trình nghiên cứu của LLM: từ hình thành ý tưởng, thiết kế thí nghiệm, viết bài báo đến phản biện ngang hàng. |
| **3** | [**The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery**](https://arxiv.org/abs/2408.06292) | Chris Lu et al. (Sakana AI & Foerster Lab) | 2024–2025 (*arXiv:2408.06292*) | Hệ thống tự động hóa khép kín toàn bộ quy trình nghiên cứu: từ sinh ý tưởng, đọc tài liệu Semantic Scholar, viết code thực nghiệm, vẽ biểu đồ, viết bài báo LaTeX và tự phản biện bằng LLM reviewer. |
| **4** | [**PaperQA2: Superhuman scientific literature search and synthesis**](https://www.nature.com/articles/s41586-024-paperqa2) | Michael Skarlinski et al. (FutureHouse) | 2024–2025 (*Nature / bioRxiv*) | Đạt độ chính xác vượt trội con người trong tìm kiếm và tổng hợp tài liệu khoa học nhờ cơ chế RAG phân mảnh nhỏ có đối chiếu chéo (chunk-level citation grounding) và loại trừ ảo giác trích dẫn. |
| **5** | [**Assisting in Writing Wikipedia-like Articles From Scratch with Large Language Models (STORM)**](https://arxiv.org/abs/2402.14207) | Yuling Shao et al. (Stanford University) | 2024 (*NAACL 2024*) | Kiến trúc nghiên cứu đa góc nhìn (Perspective-guided question asking), giả lập các cuộc phỏng vấn đa chuyên gia để khai thác tài liệu đa chiều trước khi lập dàn ý và viết bài tổng quan. |
| **6** | [**Agent Laboratory: Using LLM Agents as Research Assistants**](https://arxiv.org/abs/2501.04227) | Samuel Schmidgall et al. (Johns Hopkins University) | 2025–2026 (*arXiv:2501.04227*) | Mô hình phòng thí nghiệm đa đặc vụ (Multi-agent lab) gồm 3 chuyên viên: Literature Review Agent, Experiment Agent, và Report Writing Agent phối hợp tuần tự. |
| **7** | [**Transforming Science with Large Language Models**](https://arxiv.org/abs/2502.05151) | Steffen Eger et al. | 2025–2026 (*arXiv:2502.05151*) | Bản đồ lộ trình liên ngành đánh giá tác động của mô hình đa phương thức (Multimodal LLMs) trong đồ thị tri thức khoa học, sinh sơ đồ và chuẩn mực liêm chính học thuật. |

---

## 2. Các Kho Mã Nguồn Mở Hàng Đầu (GitHub Repositories)

### 2.1. Frameworks Nghiên Cứu & Tự Động Hóa Toàn Diện (End-to-End Agents)
* **[SakanaAI/AI-Scientist](https://github.com/SakanaAI/AI-Scientist)**:
  * *Mô tả*: Framework tự động hóa nghiên cứu mở, kết nối Semantic Scholar API, sinh thí nghiệm PyTorch/ML, biên dịch bài báo LaTeX hoàn chỉnh.
  * *Học hỏi*: Kiến trúc Tree-Search để chọn lọc ý tưởng khoa học mới và bộ chấm điểm liêm chính học thuật.
* **[SamuelSchmidgall/AgentLaboratory](https://github.com/SamuelSchmidgall/AgentLaboratory)**:
  * *Mô tả*: Phòng thí nghiệm nghiên cứu tự hành với các agent chuyên biệt: Thu thập tài liệu $\to$ Lập kế hoạch thực nghiệm $\to$ Phân tích kết quả $\to$ Soạn thảo báo cáo.
  * *Học hỏi*: Cách phân công vai trò (subagents) rõ ràng, giảm thiểu context bloat.
* **[stanford-oval/storm](https://github.com/stanford-oval/storm)**:
  * *Mô tả*: Hệ thống Stanford STORM thu thập tri thức qua tìm kiếm mạng xã hội, tài liệu mở, đối thoại đa góc nhìn và trích dẫn nguồn minh bạch.
  * *Học hỏi*: Cơ chế sinh câu hỏi đa góc nhìn (perspective prompts) để không bị thiên vị nguồn tin.

### 2.2. Công Cụ Đọc Hiểu & Tổng Hợp Học Thuật Chính Xác Cao (Precision Literature Review)
* **[Future-House/paper-qa](https://github.com/Future-House/paper-qa)**:
  * *Mô tả*: Thư viện chuẩn mực cho Agentic RAG trên PDF khoa học. Mỗi câu khẳng định đều bắt buộc gắn kèm đoạn văn chứng cứ (evidence chunk) từ tài liệu gốc.
  * *Học hỏi*: Thuật toán lọc nhiễu tài liệu và kiểm tra chéo (citation grounding) loại bỏ 100% trích dẫn giả mạo (hallucinated citations).
* **[K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)**:
  * *Mô tả*: Kỹ năng modular chuyên nghiệp để thực hiện systematic reviews qua arXiv, PubMed, bioRxiv.

### 2.3. Deep Research & Web Traversal Agents
* **[dzhng/deep-research](https://github.com/dzhng/deep-research)**:
  * *Mô tả*: Công cụ deep research mã nguồn mở mô phỏng quy trình tìm kiếm đệ quy, bóc tách trang web bằng Playwright/Firecrawl và tổng hợp báo cáo chuyên sâu.
  * *Học hỏi*: Chiến lược mở rộng từ khóa tìm kiếm theo chiều sâu (depth-first query expansion).
* **[LightChen233/Awesome-AI4Research](https://github.com/LightChen233/Awesome-AI4Research)**:
  * *Mô tả*: Danh mục tổng hợp toàn bộ các bộ dữ liệu benchmark (AIRS-Bench, SciBench), công cụ trích xuất tài liệu và mô hình AI cho nghiên cứu khoa học.
