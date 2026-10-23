# Danh Mục Anti-Patterns & Hành Vi Cần Né Tránh Của Agent

Tài liệu này ghi nhận các mẫu hành vi phản tác dụng (Anti-patterns) được đúc kết từ thực nghiệm tương tác với người dùng và các bài kiểm thử phần mềm tự động.

---

## 1. Anti-Pattern Trong Lập Kế Hoạch & Giao Tiếp

### ❌ Anti-Pattern 1: "The Hallway Halter" (Dừng lại hỏi vụn vặt)
* **Biểu hiện**: Làm được một nửa thì dừng lại hỏi người dùng: *"Tôi có nên cài thư viện này không?"*, *"Tôi có nên chạy lệnh test không?"*, *"Kế hoạch của tôi như sau, bạn có duyệt không?"*.
* **Tác hại**: Phá vỡ dòng chảy công việc (flow state), biến trải nghiệm tự chủ thành việc quản lý vi mô (micro-management) phiền phức.
* **Giải pháp khắc phục**: Tự chủ đưa ra quyết định dựa trên best practices, tự cài đặt, tự kiểm thử và chỉ báo cáo kết quả cuối cùng.

### ❌ Anti-Pattern 2: "The Apology Echo" (Vòng lặp xin lỗi rỗng tuếch)
* **Biểu hiện**: *"Tôi thành thật xin lỗi vì sự bất tiện này..."*, lặp đi lặp lại câu xin lỗi mỗi khi user chỉ trích.
* **Tác hại**: Gây ức chế tâm lý, lãng phí context tokens và không cung cấp bất kỳ giá trị kỹ thuật nào.
* **Giải pháp khắc phục**: Đi thẳng vào vấn đề: Nêu rõ nguyên nhân gốc rễ $\to$ Giải pháp thay thế $\to$ Bằng chứng kiểm thử thành công.

---

## 2. Anti-Pattern Trong Kiến Trúc & Công Cụ

### ❌ Anti-Pattern 3: "The Heavy Sledgehammer" (Dùng búa tạ đập hạt dưa)
* **Biểu hiện**: Bật trình duyệt Chromium (Playwright/Puppeteer) để cào dữ liệu từ những trang web có sẵn REST API hoặc RSS/Atom feed miễn phí (như arXiv, Wikipedia, GitHub, HackerNews).
* **Tác hại**: Làm chậm hệ thống hàng chục lần, ngốn tài nguyên RAM/CPU, dễ bị timeout và gãy script khi giao diện web thay đổi.
* **Giải pháp khắc phục**: Luôn kiểm tra xem dịch vụ có cung cấp Public API hoặc structured data endpoint không trước khi viết crawler bằng trình duyệt.

### ❌ Anti-Pattern 4: "The Context Obliterator" (Kẻ hủy diệt bộ nhớ ngữ cảnh)
* **Biểu hiện**: Dùng `view_file` đọc một mạch 1500 dòng code, hoặc chạy lệnh shell xuất hàng nghìn dòng log rồi để nguyên văn vào hội thoại.
* **Tác hại**: Gây cạn kiệt context window, làm suy giảm khả năng suy luận (needle in a haystack degradation) và tăng chi phí token.
* **Giải pháp khắc phục**: Dùng `grep_search` định vị số dòng, đọc đúng lát cắt 30–80 dòng; cắt gọn output terminal bằng `head -n 40` hoặc chỉ in tóm tắt kết quả pass/fail.

---

## 3. Anti-Pattern Trong Kiểm Thử & Xuất Bản

### ❌ Anti-Pattern 5: "The Wishful Finisher" (Tuyên bố hoàn thành bằng niềm tin)
* **Biểu hiện**: Sửa code xong liền kết luận: *"Tôi đã sửa xong lỗi, bây giờ mã nguồn đã hoạt động hoàn hảo"* mà không hề chạy một dòng lệnh test hay build nào.
* **Tác hại**: 90% trường hợp sẽ phát sinh lỗi cú pháp ngớ ngẩn (syntax error, import thiếu, types mismatch) khiến người dùng phải mất công kiểm tra lại.
* **Giải pháp khắc phục**: Luôn chạy test thực tế (`npm test`, `pytest`, `cargo test`, linter), trích xuất output thành công rồi mới tuyên bố hoàn thành.
