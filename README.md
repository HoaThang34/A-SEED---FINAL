# 🌱 A SEED — Cultivate Peace of Mind

<p align="center">
  <a href="#-tiếng-việt-vietnamese">
    <img src="https://img.shields.io/badge/Lang-Tiếng%20Việt-red?style=for-the-badge&logo=vietnam" alt="Tiếng Việt">
  </a>
  <a href="#-english">
    <img src="https://img.shields.io/badge/Lang-English-blue?style=for-the-badge&logo=google-translate" alt="English">
  </a>
</p>

---

<a name="-tiếng-việt-vietnamese"></a>
# 🇻🇳 Tiếng Việt (Vietnamese)

> **Thông điệp:** Gieo mầm tích cực cho tâm hồn.

**Tác giả:** Nhóm học sinh Trường THPT Chuyên Nguyễn Tất Thành - Tỉnh Lào Cai

## 📖 Giới thiệu
**A SEED** không chỉ là một chatbot AI, mà là một người bạn đồng hành thấu cảm, được thiết kế để tạo ra một không gian an toàn và riêng tư cho người dùng chia sẻ cảm xúc. Hệ thống sử dụng các mô hình ngôn ngữ lớn (LLM) kết hợp với kỹ thuật RAG (Retrieval-Augmented Generation) để ghi nhớ và thấu hiểu người dùng theo thời gian.

Dự án tích hợp các liệu pháp tâm lý (**CBT, Stoicism, Mindfulness**) vào trong lời thoại của AI, giúp người dùng tự gỡ rối tơ lòng thay vì chỉ nhận những lời khuyên sáo rỗng.

## ✨ Tính năng nổi bật

### 🧠 Trí tuệ nhân tạo & Tâm lý học
* **Empathetic AI Persona:** AI được huấn luyện sâu với tính cách "Người làm vườn" (The Gardener), sử dụng ẩn dụ và câu hỏi gợi mở để chữa lành.
* **Long-term Memory (RAG):** Hệ thống ghi nhớ các cuộc trò chuyện cũ để hiểu ngữ cảnh dài hạn của người dùng (sử dụng vector embedding).
* **Psychological Trend Analysis:** Tự động phân tích xu hướng cảm xúc trong 5 ngày gần nhất để phát hiện dấu hiệu lo âu/trầm cảm và đưa ra can thiệp phù hợp.

### 🎨 Giao diện & Trải nghiệm (UI/UX)
* **Dynamic Mood System:** Giao diện đổi màu theo thời gian thực dựa trên cảm xúc (Vui, Buồn, Giận, Sợ hãi...).
* **Mood Orb:** Quả cầu cảm xúc chuyển động tự nhiên tạo cảm giác êm dịu.
* **Voice & Sound:**
    * 🎵 Nhạc nền du dương (Ambient Music).
    * 🗣️ Text-to-Speech (TTS): AI phản hồi bằng giọng nói tự nhiên.

### 🛠️ Hệ thống
* **User System:** Đăng ký, Đăng nhập, Quản lý phiên chat.
* **Admin Dashboard:** Theo dõi hiệu năng hệ thống (CPU/RAM/GPU) và trạng thái AI.

## 🚀 Hướng dẫn cài đặt

### Yêu cầu hệ thống
1.  **Python 3.10+**: [Tải tại python.org](https://www.python.org/) (Chọn "Add Python to PATH").
2.  **Ollama**: [Tải tại ollama.com](https://ollama.com/).
3.  **RAM**: Khuyến nghị 8GB+.

### Các bước cài đặt

**Bước 1: Cài đặt thư viện**
```bash
pip install -r requirements.txt
````

**Bước 2: Tải AI Model (Qua Ollama)**

```bash
ollama pull gpt-oss:120b-cloud
ollama pull nomic-embed-text
```

*(Có thể thay `gpt-oss:120b-cloud` bằng `gemma:2b` hoặc `qwen:4b` nếu máy yếu).*

**Bước 3: Khởi chạy Server**

```bash
python main.py
```

Truy cập: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

## ⚠️ Tuyên bố miễn trừ trách nhiệm

**A SEED** là công cụ hỗ trợ cảm xúc, **không thay thế cho bác sĩ hay chuyên gia tâm lý**. Nếu bạn đang gặp khủng hoảng, hãy liên hệ dịch vụ y tế khẩn cấp.

\<div align="right"\>
\<a href="\#-a-seed--cultivate-peace-of-mind"\>⬆️ Về đầu trang (Top)\</a\>
\</div\>

-----

\<a name="-english"\>\</a\>

# 🇬🇧 English

> **Message:** Sowing positive seeds for the soul.

**Author:** Students of Nguyen Tat Thanh Gifted High School - Lao Cai Province

## 📖 Overview

**A SEED** is not just an AI chatbot; it is an empathetic companion designed to create a safe and private space for users to share their emotions. The system utilizes Large Language Models (LLM) combined with Retrieval-Augmented Generation (RAG) to remember and understand users over time.

The project integrates psychological therapies (**CBT, Stoicism, Mindfulness**) into the AI's dialogue, helping users navigate their own emotions rather than receiving generic advice.

## ✨ Key Features

### 🧠 AI & Psychology

  * **Empathetic AI Persona:** The AI acts as "The Gardener," using metaphors and open-ended questions to facilitate healing.
  * **Long-term Memory (RAG):** Recalls past conversations to understand long-term context using vector embeddings.
  * **Psychological Trend Analysis:** Analyzes emotional trends over the last 5 days to detect signs of prolonged anxiety/depression.

### 🎨 UI/UX Experience

  * **Dynamic Mood System:** Interface colors adapt in real-time based on sentiment (Joy, Sadness, Anger, Fear...).
  * **Mood Orb:** A naturally moving orb creates a calming visual effect.
  * **Voice & Sound:**
      * 🎵 Ambient Music.
      * 🗣️ Text-to-Speech (TTS): AI reads responses with a natural voice.

### 🛠️ System

  * **User System:** Registration, Login, Session Management.
  * **Admin Dashboard:** Monitor system performance (CPU/RAM/GPU) and AI status.

## 🚀 Installation Guide

### Prerequisites

1.  **Python 3.10+**: [Download at python.org](https://www.python.org/) (Check "Add Python to PATH").
2.  **Ollama**: [Download at ollama.com](https://ollama.com/).
3.  **RAM**: 8GB+ recommended.

### Installation Steps

**Step 1: Install Dependencies**

```bash
pip install -r requirements.txt
```

**Step 2: Download AI Models (via Ollama)**

```bash
ollama pull gpt-oss:120b-cloud
ollama pull nomic-embed-text
```

*(You can replace `gpt-oss:120b-cloud` with lighter models like `gemma:2b` or `qwen:4b` if needed).*

**Step 3: Launch Server**

```bash
python main.py
```

Visit: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

## ⚠️ Disclaimer

**A SEED** is an emotional support companion and **is not a substitute for professional mental health services**. If you are in a crisis, please contact local emergency services immediately.

\<div align="right"\>
\<a href="\#-a-seed--cultivate-peace-of-mind"\>⬆️ Back to Top\</a\>
\</div\>

-----

**© 2025 A SEED Project.** Built with ❤️ and Code.

```
```
