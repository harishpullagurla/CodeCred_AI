# 🤖 CodeCred AI | AI Skill Verification Tool
**CodeCred AI** is an AI-powered skill verification tool that compares a candidate’s **resume claims** with their **actual GitHub work**.

It analyzes repositories, dependencies, and coding patterns to identify real technical skills and highlight gaps between what someone claims and what their code demonstrates.

This makes it useful for:

- Recruiters validating developer skills  
- Students checking portfolio authenticity  
- Developers showcasing verified expertise  

---

## 🚀 Key Features

### 🔎 Skill Verification from GitHub
- Scans repositories, languages, and dependency files.
- Detects frameworks, databases, and technologies used in projects.
- Matches them against resume skills.



### 🧠 AI-Powered Insights
- Uses Google Gemini AI for intelligent analysis.
- Generates a structured report including:
  - ✅ Verified Skills  
  - ⚠️ Claimed but Not Found Skills  
  - 💡 Additional Skills Detected  

---

## 🛠️ Tech Stack

**Backend**
- Python (Flask)

**AI Engine**
- Google Gemini API

**Data Processing**
- GitHub REST API
- PDF text extraction (`pypdf`)

**Frontend**
- HTML5 + Bootstrap 5

---

## 📂 Project Structure

```bash
CodeCred_AI
│
├── app.py
├── requirements.txt
├── Procfile
├── .gitignore
│
├── services
│   ├── ai_service.py
│   ├── github_service.py
│   └── pdf_service.py
│
└── templates
    └── index.html
````

---

## ⚡ Setup & Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/codecred-ai.git
cd codecred-ai
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file:

```env
GITHUB_TOKEN=your_github_token
GEMINI_API_KEY=your_gemini_api_key
```

### 4. Run the Application

```bash
python app.py
```

Server runs at:

```
http://127.0.0.1:5000
```

---

## 📊 How It Works

1. Extracts skills from the resume PDF.
2. Fetches GitHub repositories and code metadata.
3. Detects technologies, frameworks, and coding patterns.
4. Uses AI to generate a verification report comparing claims vs reality.

---
