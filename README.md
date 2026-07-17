

https://github.com/user-attachments/assets/301ebd93-d93e-4291-a413-8711d540116e





# 🧠 ResearchAI

> An AI-powered Research Paper Assistant built using Retrieval-Augmented Generation (RAG), FastAPI, React, Qdrant, and Groq.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)
![Vite](https://img.shields.io/badge/Vite-Build-646CFF?logo=vite)
![Qdrant](https://img.shields.io/badge/Qdrant-VectorDB-red)
![Groq](https://img.shields.io/badge/Groq-LLM-black)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 Overview

ResearchAI is a full-stack Retrieval-Augmented Generation (RAG) application that allows users to upload PDF research papers and interact with them using natural language.

Instead of relying solely on an LLM's pre-trained knowledge, the application retrieves the most relevant sections from the uploaded document using semantic search and supplies them as context to the language model. This enables grounded, document-specific answers with source attribution.

---

## ✨ Features

- 📄 Upload PDF research papers
- ✂️ Automatic text extraction and chunking
- 🧠 Semantic embeddings generation
- 🔍 Vector similarity search using Qdrant
- 🤖 AI-powered question answering with Groq LLM
- 📚 Source chunk citations
- 💬 Interactive chat interface
- 🗂 Multiple document support
- 🚀 FastAPI backend
- ⚛️ React + Vite frontend
- ☁️ Deployed on Render & Vercel

---

## 🏗 System Architecture

```text
                PDF Upload
                     │
                     ▼
             PDF Text Extraction
                     │
                     ▼
             Text Chunking Service
                     │
                     ▼
            Embedding Generation
      (BAAI/bge-small-en-v1.5)
                     │
                     ▼
              Qdrant Vector DB
                     │
         User Question + Embedding
                     │
                     ▼
         Semantic Similarity Search
                     │
             Top-K Relevant Chunks
                     │
                     ▼
            Groq Llama Language Model
                     │
                     ▼
             AI Generated Response
                     │
                     ▼
             React Chat Interface
```

---

# 🛠 Tech Stack

## Frontend

- React
- Vite
- CSS3
- Axios
- Lucide React
- Framer Motion

## Backend

- FastAPI
- Python
- Uvicorn

## AI / ML

- Sentence Transformers
- BAAI/bge-small-en-v1.5
- Groq API
- Llama 3
- Retrieval-Augmented Generation (RAG)

## Database

- Qdrant Vector Database

---

# 📂 Project Structure

```
ai-research-assistant/
│
├── backend/
│   ├── app/
│   ├── api/
│   ├── services/
│   ├── models/
│   └── main.py
│
├── frontend/
│   ├── src/
│   ├── api/
│   ├── assets/
│   └── App.jsx
│
├── README.md
└── requirements.txt
```
# ⚠ Known Limitations

The public demo is hosted on Render's free tier, which provides limited memory. Large PDF documents may exceed the available resources during embedding generation.

When deployed on a higher-memory instance or run locally, the application supports significantly larger documents.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Krunal Deshmukh**

AI Engineer | Artificial Intelligence & Data Science
LinkedIn: www.linkedin.com/in/krunaldeshmukh5

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

It helps others discover the project and supports future development.

---

<p align="center">
Built with ❤️ using FastAPI, React, Qdrant and Groq
</p>
