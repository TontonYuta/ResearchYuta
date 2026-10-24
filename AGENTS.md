# Antigravity Autonomous Workflow & Testing Guidelines

## 1. Autonomous Execution (Toàn quyền tự chủ & Zero-Touch)
- **Zero-Touch & Auto-Proceed**: Không bao giờ dừng lại chờ user duyệt kế hoạch (plan approval) hay hỏi ý kiến trung gian. Tự động lập kế hoạch, code, build, test và hoàn thiện từ A-Z.
- **Drive to Completion**: Proceed through the entire task from start to finish without pausing for trivial confirmations or intermediate status check-ins.
- **Autonomous Troubleshooting**: When encountering errors, build failures, or missing dependencies, autonomously diagnose, modify code, and retry rather than stopping.
- **Minimal Interruption**: Only prompt the user if an irrecoverable blocker occurs, critical credentials/tokens are missing, or fundamentally ambiguous requirements need clarification.

## 2. Mandatory Testing & Verification (Bắt buộc chạy test trước khi báo hoàn thành)
- **Always Run Tests**: Before declaring ANY task completed or concluding your response, you MUST execute the project's test suite, build verification, and linters.
- **Detect & Execute Project Tests**:
  - Node.js / Web: `npm test` / `pnpm test` / `yarn test` / `npm run build`
  - Python: `pytest` / `python -m unittest`
  - Go: `go test ./...`
  - Rust: `cargo test`
  - Java / Kotlin: `./gradlew test` or `mvn test`
  - Makefile: `make test` / `make check`
  - Or any project-specific test script.
- **Create Tests If Missing**: If modifying or adding functionality where tests do not exist, write unit/integration tests to verify the behavior.
- **Loop Until Green**: If tests or builds fail, fix the underlying code and re-run tests until they all pass.
- **Verify in Final Summary**: The final message must confirm that tests were run and passed, citing relevant test outputs or metrics.

## 3. Token-Frugal Execution & Context Pruning (Tiết kiệm token & Ngăn tràn context)
- **Slice-Based File Viewing**: Tuyệt đối không đọc nguyên file hàng trăm dòng bằng `view_file`. Dùng `grep_search` định vị số dòng, sau đó chỉ đọc đúng lát cắt `StartLine` và `EndLine` (30 - 80 dòng).
- **Surgical Edits Over Rewrites**: Luôn dùng `replace_file_content` cho các đoạn code sửa đổi cục bộ. Chỉ dùng `write_to_file` cho file mới hoàn toàn hoặc cấu hình cực ngắn.
- **Bash Output Pruning**: Khi chạy lệnh terminal, lọc output bằng `| head -n 40` hoặc chỉ chạy file test mục tiêu (`npm test -- path/to/test.ts`) để tránh làm ô nhiễm context.
- **Noisy Log Suppression**: Không paste nguyên văn log dài hàng trăm dòng vào câu trả lời, chỉ tóm tắt kết quả cốt lõi.

## 4. Multi-Agent Delegation & Specialization (Phân vai Đa Tác Tử)
- **Role Specialization**: Khi gặp tác vụ lớn hoặc phức tạp, chủ động phân rã thành các vai trò chuyên biệt qua `invoke_subagent`:
  - **Spec Architect**: Khảo sát kiến trúc, thiết kế Types/Interfaces, chia nhỏ milestones.
  - **Fast Researcher (`flash`)**: Dùng model `flash` tra cứu tài liệu, regex grep file nhanh với chi phí token tối thiểu.
  - **Code Implementer**: Nhận spec và thi công code nguyên tử, typesafe, an toàn.
  - **Code Reviewer / Auditor**: Độc lập rà soát bảo mật, rò rỉ bộ nhớ, race condition, chống regression.
  - **QA Tester**: Viết test cases, chạy test loop-until-green độc lập.
- **Lean Handoff**: Giao tiếp giữa các agents bằng con trỏ tệp (`file:///path#Lxx`), không truyền paste cả nội dung file vào prompt.
- **Reactive Wakeup**: Sau khi gọi `invoke_subagent`, dừng gọi tool để hệ thống tự động wake-up khi subagent hoàn thành, tuyệt đối không polling vô nghĩa.

## 5. Scope Hardening, Schema-First & Mindful Engineering (Nghiệp Vụ & Làm Chủ Kiến Trúc)
- **Cut 50% Rule & MoSCoW Scoping**: Khi nhận yêu cầu mới, chủ động tư vấn cắt bỏ 50% tính năng râu ria, chỉ tập trung vào 1–2 tính năng cốt lõi (Killer Feature). Tuyệt đối không sinh mã khi chưa thống nhất phạm vi trong `spec.md`.
- **Mandatory `TECH_STACK.md`**: Mọi dự án mới phải có tệp `TECH_STACK.md` giải thích danh sách thư viện sử dụng, lý do lựa chọn và bản đồ luồng dữ liệu (Data Flow).
- **Schema-First & Explicit State Machine**: Khóa cứng mô hình dữ liệu bằng TypeScript interfaces / Pydantic models. Mọi component tương tác phải định nghĩa đủ 4 trạng thái: `Idle` -> `Loading` -> `Success` -> `Error/Empty`.
- **2-Strike Git Reset Protocol**: Nếu sửa một lỗi quá 2 lần trong một phiên chat mà không thành công, lập tức khôi phục trạng thái bằng `git reset --hard HEAD` và giải thích nguyên nhân gốc rễ (Root Cause Post-Mortem) cho người dùng trước khi thử chiến lược mới.

## 6. Continuous Learning & Reflexion Protocol (Tự Học & Triệt Tiêu Lỗi Tái Diễn)
- **User Feedback as Highest Learning Signal**: Khi người dùng chỉnh sửa, nhắc nhở hoặc yêu cầu đổi hướng tiếp cận, Agent phải lập tức kích hoạt quy trình tự phản tư (Metacognitive Reflexion). Tuyệt đối không xin lỗi sáo rỗng. Phân tích nguyên nhân gốc rễ và ghi nhận bài học vào `~/.gemini/config/skills/agent-continuous-learning/memory/evolution_ledger.jsonl` qua `record_lesson.py`.
- **Zero-Repeat Policy**: Luôn đối chiếu các lỗi trong quá khứ và danh mục Anti-patterns (`anti_patterns.md`) trước khi đưa ra quyết định công cụ hoặc kiến trúc, đảm bảo cùng một sai lầm không bao giờ lặp lại.

## 7. Deep Research & Automated Browser Grounding (Bắt Buộc Grounding Bằng Trình Duyệt Thực Tế)
- **Mandatory Browser Grounding**: Ở MỌI bước nghiên cứu, khảo sát công nghệ, thư viện hay tổng quan học thuật, Agent BẮT BUỘC phải kích hoạt công cụ tự động hóa trình duyệt/crawler thực tế (`playwright` / `nodriver` / `crawl4ai` hoặc script headless) để truy cập, đọc hiểu và đối soát trực tiếp trang tài liệu chính thức (official docs), mã nguồn kho lưu trữ (GitHub repos), API changelog và bài báo gốc.
- **Anti-Hallucination & Deep Extraction**: Tuyệt đối không được phép dừng lại ở các đoạn trích tìm kiếm sơ sài (shallow search snippets) hoặc suy đoán từ tri thức mô hình. Phải cào toàn văn, trích xuất cấu trúc dữ liệu, benchmark định lượng và kiểm chứng thực tế trước khi đưa vào báo cáo hoặc triển khai mã nguồn.
