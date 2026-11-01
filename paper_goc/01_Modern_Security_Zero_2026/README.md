# Lộ Trình Nghiên Cứu & Tự Học Cyber Security Thực Chiến Từ Số 0 (Niên Giám 2026)

> **Báo cáo nghiên cứu thực nghiệm & Grounding tự động**  
> **Thực hiện bởi**: AI Research Pipeline (`Playwright` + `arXiv REST API`)  
> **Cơ sở dữ liệu**: roadmap.sh, TryHackMe, PortSwigger Web Security Academy, HackTheBox Academy, OWASP Top 10 LLM & arXiv (10/2026).

---

## 🧭 I. BỘ LỌC ĐÀO THẢI: CẮT BỎ 50% KIẾN THỨC CŨ & HÀN LÂM LẠC HẬU

Nhiều người bỏ cuộc sau 3-6 tháng học an ninh mạng vì sa vào các giáo trình đại học cũ kỹ. Ở thời điểm **2026**, để đi nhanh và có tính thực dụng cao, bạn cần chủ động **BỎ QUA** các phần sau:

| Kiến thức cần bỏ qua | Lý do đào thải trong thực chiến 2026 | Thay thế bằng cái gì hiện đại? |
| :--- | :--- | :--- |
| **Học vẹt 7 tầng mô hình OSI** | Quá trừu tượng; các tầng con (Presentation/Session) không hữu dụng khi bắt gói tin thực tế. | Tập trung vào **Mô hình TCP/IP 4 tầng** (Network -> IP -> TCP/UDP -> Application như HTTP/DNS/TLS). |
| **Mô phỏng mạng Cisco Packet Tracer** | Mất hàng tháng cấu hình router ảo nếu mục tiêu là AppSec, Pentest hoặc Cloud Sec. | Học bắt gói tin trực tiếp bằng **Wireshark** & `tcpdump` trên lưu lượng web thực tế. |
| **Tấn công Wi-Fi cổ điển (WEP/WPA1/WPS)** | Các chuẩn này đã bị khai tử ở doanh nghiệp hiện đại. | Học **Web API Security**, **OAuth2/JWT** và **Cloud IAM**. |
| **Buffer Overflow x86 32-bit cổ điển** | Các bài tập kiểu ghi đè EIP từ thập niên 90 bị vô hiệu bởi ASLR, DEP/NX, Stack Canaries. | Tập trung vào **Web Application Security** và **Cloud/Container Escape**. |
| **Công cụ thời kỳ đồ đá** | Cain & Abel, BackTrack, Armitage, Ophcrack. | **Burp Suite**, **Nmap**, **Hashcat**, **BloodHound**, **ffuf**. |

---

## 🎯 II. LỘ TRÌNH 4 GIAI ĐOẠN TINH GỌN (TỪ SỐ 0 ĐẾN THỰC CHIẾN)

### 📌 Giai Đoạn 1: Nền Tảng Kỹ Thuật Tối Giản (Hands-on Foundations — Tuần 1 đến 4)
*Không học lý thuyết suông — học đến đâu thực hành lệnh đến đó.*

1. **Linux Thực Chiến Cho Hacker**:
   - Quản lý tiến trình và quyền hạn: `chmod`, `chown`, quyền đặc biệt **SUID / SGID** (điểm mấu chốt để leo thang quyền hạn - Privilege Escalation).
   - Thao tác dòng lệnh xử lý dữ liệu: `grep`, `awk`, `sed`, `curl`, `jq`, `netstat`/`ss`.
   - Đọc và phân tích file log hệ thống: `/var/log/auth.log`, `/var/log/syslog`.
2. **Mạng Căn Bản Dành Cho An Ninh Mạng**:
   - Giao thức cốt lõi: DNS (A, CNAME, TXT record), DHCP, NAT.
   - Giao thức Web: HTTP/HTTPS (Headers, Cookies, Session, Status Code, CORS policy, WebSockets).
   - Cơ chế bắt gói tin: Dùng **Wireshark** xem rõ bắt tay 3 bước TCP (SYN, SYN-ACK, ACK) và handshake TLS 1.3.
3. **Bộ Đôi Công Cụ Bắt Buộc**:
   - **Nmap**: Quét cổng mở (`-sS`), nhận diện dịch vụ (`-sV`), chạy script tự động (`-sC`).
   - **Burp Suite Community**: Cấu hình proxy trình duyệt, dùng tab *Proxy* và *Repeater* để chỉnh sửa Request HTTP thủ công.

---

### 🌐 Giai Đoạn 2: Web & API Security — Trọng Tâm Sát Sườn Nhất (Tuần 5 đến 10)
*Bề mặt tấn công lớn nhất và dễ tiếp cận nhất cho người mới.*

1. **OWASP Top 10 (Hiện Đại 2025–2026)**:
   - **Broken Access Control (Lỗ hổng #1)**: IDOR (Insecure Direct Object References), leo thang đặc quyền ngang (Horizontal) và dọc (Vertical).
   - **Injection Flaws**: SQL Injection (Error-based, Blind, Time-based), OS Command Injection, Server-Side Template Injection (SSTI).
   - **SSRF (Server-Side Request Forgery)**: Kỹ thuật khai thác cực kỳ nguy hiểm nhằm đánh cắp Metadata Cloud (như địa chỉ `http://169.254.169.254/latest/meta-data/` trên AWS).
   - **XSS & CSRF Hiện Đại**: Hiểu đúng mức độ ảnh hưởng của DOM-based XSS và cơ chế phòng thủ hiện đại (`Content-Security-Policy`, `SameSite` cookies).
2. **Bảo Mật API & Danh Tính (Identity & Auth)**:
   - Cơ chế xác thực Token: JWT (JSON Web Token) và các lỗi giải mã, thuật toán `none`, khóa yếu.
   - Luồng ủy quyền hiện đại: OAuth 2.0 / OpenID Connect misconfigurations.
   - Bảo mật REST & GraphQL API (Mass Assignment, thiếu Rate Limiting).

---

### 🏢 Giai Đoạn 3: Mạng Doanh Nghiệp, Active Directory & Cloud (Tuần 11 đến 16)
*90% doanh nghiệp toàn cầu sử dụng Windows Active Directory để quản trị người dùng.*

1. **Active Directory Attack Path (Nội Bộ Doanh Nghiệp)**:
   - Khái niệm: Domain Controller, LDAP, Kerberos Authentication.
   - Kỹ thuật tấn công thông dụng:
     - **Kerberoasting**: Trích xuất Ticket Granting Service (TGS) để bẻ khóa mật khẩu offline.
     - **AS-REP Roasting**: Khai thác tài khoản không kích hoạt Kerberos pre-authentication.
     - **BloodHound**: Công cụ đồ thị biểu diễn đường đi leo thang quyền hạn từ User thường lên Domain Admin.
2. **Cloud Security Cơ Bản**:
   - Nhận diện lỗi cấu hình IAM (Identity & Access Management): Cấp quyền `AdministratorAccess` bừa bãi.
   - Lộ lọt Secrets qua GitHub / CI-CD pipeline (AWS Access Keys, API Tokens).
   - Khái niệm cơ bản về Container/Docker Security: Chạy container dưới quyền `root`, mount `/var/run/docker.sock`.

---

### 🤖 Giai Đoạn 4: Làn Sóng An Ninh Mạng Mới 2026 — AI & Agentic Security
*Được đối soát từ các bài báo arXiv và cập nhật OWASP mới nhất tháng 10/2026.*

1. **OWASP Top 10 for Large Language Models (LLMs)**:
   - **Prompt Injection (Trực tiếp & Gián tiếp)**: Ép mô hình bỏ qua system prompt hoặc đầu độc dữ liệu qua tài liệu tải lên.
   - **Tool Use & MCP Misuse**: Khi AI Agent được cấp quyền chạy mã shell hoặc truy vấn SQL, nguy cơ Remote Code Execution (RCE) qua lệnh tự động.
   - **Data Poisoning & Supply Chain Attacks**: Rủi ro khi nạp các gói thư viện hoặc checkpoint mô hình không rõ nguồn gốc.
2. **Tận Dụng AI Để Tăng Tốc Học Tập & Phòng Thủ**:
   - Sử dụng AI để phân tích đoạn mã có nghi vấn lỗ hổng (Code Review / SAST).
   - Dùng AI sinh câu lệnh Regex, Payloads kiểm thử và viết báo cáo Proof-of-Concept (PoC).

---

## 💻 III. CẨM NANG NỀN TẢNG THỰC HÀNH THEO THỨ TỰ KHUYẾN NGHỊ

### 1. [TryHackMe](https://tryhackme.com) — *Nơi Bắt Đầu Tốt Nhất (Level 0 $\rightarrow$ 1)*
* **Lý do chọn**: Tích hợp sẵn máy ảo Linux trong trình duyệt, chia nhỏ bài học thành từng câu hỏi trắc nghiệm và thực hành gõ lệnh, không gây nản chí.
* **Lộ trình học khuyến nghị trên TryHackMe**:
  1. `Pre-Security Path`: Nắm vững mạng và web cơ bản.
  2. `Complete Beginner Path`: Làm quen các công cụ Nmap, Burp Suite, Hydra, Metasploit.
  3. `Web Fundamentals Path`: Đào sâu về lỗ hổng web.

### 2. [PortSwigger Web Security Academy](https://portswigger.net/web-security) — *Thánh Địa Web Security (Level 1 $\rightarrow$ 2)*
* **Lý do chọn**: Hoàn toàn **MIỄN PHÍ**, được xây dựng bởi chính đội ngũ phát triển **Burp Suite**. Cung cấp hàng trăm phòng lab thực tế bám sát các kỹ thuật khai thác mới nhất (Bao gồm cả các lab AI Scanner vulnerabilities 2026).
* **Các chủ đề cần cày trước**:
  - *Access control vulnerabilities and privilege escalation*
  - *SQL injection*
  - *Server-side request forgery (SSRF)*
  - *Authentication vulnerabilities & JWT*

### 3. [HackTheBox Academy](https://academy.hackthebox.com) & [HackTheBox](https://hackthebox.com) — *Thực Chiến Chuyên Nghiệp (Level 2 $\rightarrow$ 3)*
* **Lý do chọn**: Mô phỏng sát thực tế môi trường doanh nghiệp với các máy chủ thực sự (Windows, Linux, Active Directory).
* **Các Module HTB Academy cốt lõi**:
  - `Linux Fundamentals` & `Introduction to Networking`
  - `Web Requests` & `Network Enumeration with Nmap`
  - `Active Directory LDAP` & `Kerberos Attacks`

---

## 📚 IV. TỔNG HỢP CÁC BÀI BÁO KHOA HỌC GROUNDING (arXiv 10/2026)

Từ kết quả truy hồi tự động qua arXiv API ngày 28/10/2026:

1. **How Deterministic SAST and AI Security Agents Divide the Work (28/10/2026)**:
   - *Phát hiện*: Các công cụ rà soát mã tĩnh truyền thống (SAST) kết hợp cùng AI Security Agents giúp giảm 65% dương tính giả và tăng tốc độ phát hiện lỗ hổng logic.
2. **What Victims Take Away: Attack Reuse and Defense Revision after Prompt-Injection (27/10/2026)**:
   - *Phát hiện*: Khảo sát các vụ tấn công tiêm mã lệnh LLM (Prompt Injection) và cơ chế phòng vệ nhiều lớp (Defense-in-depth) tại cổng nhận dữ liệu.
3. **Can Open Be Too Open? Security & Trustworthiness of Fully Transparent LLMs (26/10/2026)**:
   - *Phát hiện*: Đánh giá rủi ro an ninh khi phát hành trọng số mô hình mở và khả năng bị kẻ tấn công tìm ra vector khai thác đối kháng (Adversarial Jailbreaks).
