# Sách Lược Tự Phản Tư & Học Tăng Cường Ngôn Ngữ (Reflexion Protocol)

Tài liệu này tổng hợp cơ sở lý thuyết và phương pháp luận triển khai kỹ thuật **Reflexion (Verbal Reinforcement Learning)** cho các Agent tự chủ.

---

## 1. Cơ Chế Hoạt Động Của Reflexion

Trong các hệ thống học máy truyền thống, Reinforcement Learning (RL) cập nhật trọng số số học (Numeric Weights via Gradient Descent). Trong khi đó, **Reflexion** cập nhật **bộ nhớ ngôn ngữ (Verbal Memory Buffers)**:

1. **Actor**: Sinh hành vi / mã nguồn dựa trên bối cảnh hiện tại.
2. **Evaluator**: Đo lường kết quả (dựa trên test suite, linter hoặc phản hồi của người dùng).
3. **Self-Reflection (Phản tư)**:
   * Nếu kết quả thất bại, mô hình chuyển đổi tín hiệu lỗi thành một đoạn nhận thức ngôn ngữ chi tiết (Verbal Reflection).
   * Đoạn nhận thức này lưu vào bộ nhớ làm việc hoặc bộ nhớ dài hạn, đóng vai trò là "Kinh nghiệm xương máu" cho các lần thử tiếp theo.

```mermaid
sequenceDiagram
    participant User/Env as Môi trường / User
    participant Actor as Agent (Actor)
    participant Evaluator as Đánh giá (Evaluator)
    participant Memory as Bộ nhớ (Memory Ledger)

    Actor->>User/Env: Thực thi hành động / Tạo code
    User/Env->>Evaluator: Kết quả (Test fail / User chỉnh sửa)
    Evaluator->>Actor: Báo cáo lỗi & Tín hiệu phản hồi
    Actor->>Actor: Metacognitive Reflexion (Tự vấn)
    Actor->>Memory: Ghi nhận bài học (Lesson Distilled)
    Memory->>Actor: Tiêm tri thức mới vào bối cảnh các lần sau
```

---

## 2. Thang Đo Độ Sâu Nhận Thức (Reflexion Depth Levels)

| Cấp độ | Tên gọi | Bản chất | Ví dụ hành vi |
| :--- | :--- | :--- | :--- |
| **L0** | Phản ứng vô thức | Xin lỗi suông, không có lý do | *"Tôi xin lỗi, tôi sẽ thử lại"* (Và lại lặp lại lỗi cũ). |
| **L1** | Nhận diện triệu chứng | Chỉ thấy bề mặt lỗi cú pháp | *"Lỗi do thiếu dấu phẩy ở dòng 12, tôi đã thêm dấu phẩy"*. |
| **L2** | Phân tích nguyên nhân | Nhìn ra lỗi logic hoặc thiết kế | *"Tôi đã dùng sai hàm API vì tài liệu phiên bản v3 đã thay đổi chữ ký hàm"*. |
| **L3** | Khái quát hóa quy tắc | Đúc kết thành nguyên lý hành vi | *"Các thư viện lớn luôn có breaking changes giữa các major version; từ nay phải luôn kiểm tra version trong package.json trước khi import"*. |
| **L4** | Tiến hóa hệ thống | Tự động cập nhật vào Rules & Tooling | *Tự động ghi vào AGENTS.md và thêm test case tự động phát hiện lỗi tương tự*. |

> [!TIP]
> Mục tiêu của Agent là luôn đạt **Cấp độ L3 và L4**: Không bao giờ dừng lại ở việc sửa chữa cục bộ mà phải tổng quát hóa thành quy tắc ngăn chặn lỗi tái diễn.
