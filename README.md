# 🌱 A SEED — Cultivate Peace of Mind

**Dự án bởi:** Nhóm học sinh Trường THPT Chuyên Nguyễn Tất Thành - Tỉnh Lào Cai
**Thông điệp:** Gieo mầm tích cực cho tâm hồn.

-----

## 📖 Giới thiệu (Overview)

**A SEED** không chỉ là một chatbot AI, mà là một người bạn đồng hành thấu cảm, được thiết kế để tạo ra một không gian an toàn và riêng tư cho người dùng chia sẻ cảm xúc. Hệ thống sử dụng các mô hình ngôn ngữ lớn (LLM) kết hợp với kỹ thuật RAG (Retrieval-Augmented Generation) để ghi nhớ và thấu hiểu người dùng theo thời gian.

Dự án tích hợp các liệu pháp tâm lý (CBT, Stoicism, Mindfulness) vào trong lời thoại của AI, giúp người dùng tự gỡ rối tơ lòng thay vì chỉ nhận lời khuyên sáo rỗng.

-----

## ✨ Tính năng nổi bật (Key Features)

### 🧠 Trí tuệ nhân tạo & Tâm lý học

  * **Empathetic AI Persona:** AI được huấn luyện sâu với tính cách "Người làm vườn" (The Gardener), sử dụng ẩn dụ và câu hỏi gợi mở để chữa lành.
  * **Long-term Memory (RAG):** Hệ thống ghi nhớ các cuộc trò chuyện cũ để hiểu ngữ cảnh dài hạn của người dùng (sử dụng vector embedding).
  * **Psychological Trend Analysis:** Tự động phân tích xu hướng cảm xúc của người dùng trong 5 ngày gần nhất để phát hiện dấu hiệu lo âu/trầm cảm kéo dài và đưa ra can thiệp phù hợp.

### 🎨 Giao diện & Trải nghiệm (UI/UX)

  * **Dynamic Mood System:** Giao diện và màu sắc thay đổi theo thời gian thực dựa trên cảm xúc của cuộc trò chuyện (Vui, Buồn, Giận, Sợ hãi...).
  * **Mood Orb:** Quả cầu cảm xúc chuyển động tự nhiên tạo cảm giác êm dịu.
  * **Dark/Light Mode:** Chế độ Sáng/Tối linh hoạt.
  * **Voice & Sound:**
      * 🎵 Nhạc nền du dương (Ambient Music).
      * 🗣️ Text-to-Speech (TTS): AI có thể đọc phản hồi bằng giọng nói tự nhiên (hỗ trợ Tiếng Việt & Tiếng Anh).

### 🛠️ Hệ thống & Quản trị

  * **User System:** Đăng ký, Đăng nhập, Quản lý phiên chat (Session).
  * **Mood Statistics:** Biểu đồ thống kê cảm xúc giúp người dùng theo dõi sức khỏe tinh thần.
  * **Admin Dashboard:** Theo dõi hiệu năng hệ thống (CPU, RAM, GPU), trạng thái AI Model và quản lý server.

-----

## ⚙️ Yêu cầu hệ thống (Prerequisites)

Để chạy dự án, máy tính cần cài đặt:

1.  **Python 3.10+**: [Tải tại python.org](https://www.python.org/) (Nhớ tích chọn "Add Python to PATH").
2.  **Ollama**: [Tải tại ollama.com](https://ollama.com/) (Dùng để chạy AI Model offline).
3.  **RAM**: Khuyến nghị 8GB trở lên (16GB nếu dùng model lớn).
4.  **GPU (Tuỳ chọn)**: Để AI phản hồi nhanh hơn.

-----

## 🚀 Hướng dẫn cài đặt (Installation Guide)

### Bước 1: Chuẩn bị mã nguồn

Tải và giải nén thư mục dự án `A-SEED---FINAL`.

### Bước 2: Cài đặt thư viện Python

Mở Terminal (hoặc CMD/PowerShell) tại thư mục dự án và chạy lệnh:

```bash
pip install -r requirements.txt
```

### Bước 3: Cài đặt AI Model (Thông qua Ollama)

Mở Terminal và chạy các lệnh sau để tải model về máy (cần kết nối mạng):

1.  Tải model ngôn ngữ chính:

    ```bash
    ollama pull gpt-oss:120b-cloud
    ```

    *(Lưu ý: Nếu máy yếu, bạn có thể thay bằng model nhẹ hơn như `gemma:2b` hoặc `qwen:4b` trong file `main.py`)*

2.  Tải model xử lý bộ nhớ (Embedding):

    ```bash
    ollama pull nomic-embed-text
    ```

### Bước 4: Khởi chạy Server

Tại thư mục dự án, chạy lệnh:

```bash
python main.py
```

*(Hoặc `python main_server.py` nếu muốn chạy phiên bản tối giản không có TTS).*

Khi thấy dòng chữ `Server is live...`, hãy mở trình duyệt và truy cập:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

-----

## 💡 Hướng dẫn sử dụng

### 1\. Người dùng (User)

  * **Đăng ký/Đăng nhập:** Tạo tài khoản để lưu trữ lịch sử chat riêng tư.
  * **Trò chuyện:** Nhập tin nhắn hoặc dùng Micro 🎙️ để nói chuyện.
  * **Công cụ:**
      * `🔊 Music On/Off`: Bật tắt nhạc nền.
      * `🗣️ Voice On/Off`: Bật tắt tính năng AI đọc tin nhắn.
      * `📊 Mood Stats`: Xem biểu đồ cảm xúc phiên hiện tại.
      * `History`: Xem lại các đoạn chat cũ.

### 2\. Quản trị viên (Admin)

Truy cập vào đường dẫn: **[http://127.0.0.1:8000/admin](https://www.google.com/search?q=http://127.0.0.1:8000/admin)**

  * **Tài khoản mặc định:**
      * Username: `admin`
      * Password: `admin123`
  * **Chức năng:** Xem uptime, tài nguyên hệ thống (CPU/RAM/GPU), trạng thái kết nối Ollama và khởi động lại server.

-----

## 📂 Cấu trúc thư mục

```text
A-SEED/
├── data/               # Chứa dữ liệu người dùng, lịch sử chat, bộ nhớ vector
├── static/             # CSS, JS, hình ảnh, âm thanh
│   ├── style.css       # Giao diện chính (Glassmorphism)
│   ├── motion.css      # Hiệu ứng chuyển động
│   ├── app.js          # Logic Frontend
│   └── ...
├── templates/          # Các file HTML (Login, Chat, Admin)
├── training/           # Dữ liệu huấn luyện tính cách AI (System Prompt)
├── main.py             # Server chính (Full tính năng: TTS, RAG, Trends)
├── main_server.py      # Server phiên bản clean code
├── requirements.txt    # Danh sách thư viện
└── README.md           # Hướng dẫn sử dụng
```

-----

## ⚠️ Tuyên bố miễn trừ trách nhiệm (Disclaimer)

**A SEED** là một người bạn đồng hành hỗ trợ cảm xúc, **không phải là sự thay thế cho các dịch vụ chăm sóc sức khỏe tâm thần chuyên nghiệp**. Nếu bạn đang trong tình trạng khủng hoảng hoặc có ý định làm hại bản thân, vui lòng liên hệ ngay với các dịch vụ khẩn cấp tại địa phương hoặc người thân.

-----

**© 2025 A SEED Project.** Built with ❤️ and Code.

