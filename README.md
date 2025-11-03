# Advanced Plagiarism Checker (Academic Grade)

## Overview

This is a full-stack academic plagiarism detection system developed for B.Tech Computer Science as a professional institutional project. It performs plagiarism checks using both local document comparison (Cosine Similarity, ML) and Internet Search (Google Custom Search API). The system delivers both real-time highlighted web results and downloadable academic-style PDF reports.

- Streamlit web UI with side-by-side text highlighting
- Color-coded plagiarism levels (Turnitin style)
- Professional, institution-grade PDF reports with all details
- Robust `.gitignore` and `.env` handling for secure cloud and local deployment

## Features

- **Side-by-side Document Comparison:** Instantly compare source and submission documents with interactive yellow highlights of matches.
- **Internet Search Plagiarism Check:** Uses Google CSE API to check your content against the open web.
- **Professional Plagiarism Reports:** One-click PDF generation formatted for college/university standards, including color legends and verdicts.
- **Modern Security:** All API keys and private configs are kept in `.env` (included in `.gitignore`, never upload them!).
- **Docker Ready, Cloud Ready:** Built for easy deployment anywhere.

---

## Folder Structure

```
project-root/
│
├── backend_api/
│     ├── professional_pdf_generator.py
│     ├── model.py
│     ├── file_handler.py
│     ├── data_prep.py
│     └── ...
│
├── frontend_app/
│     ├── app_ultimate.py
│     └── ...
│
├── sample_data/
│     ├── plagiarism_dataset.csv
│     └── ...
│
├── .env.example           # Populate and rename to .env (do not upload yours)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Quick Start

### 1. Prerequisites

- Python 3.9+
- [pip](https://pip.pypa.io/en/stable/)
- Google Custom Search and API keys (for Internet plagiarism mode)

### 2. Clone and Setup

```bash
git clone <YOUR_REPO_URL>
cd <project-root>
pip install -r requirements.txt
```

### 3. Environment Variables

Copy `.env.example` to `.env` and fill in your sensitive credentials:

```
GOOGLE_API_KEY=your_key_here
SEARCH_ENGINE_ID=your_id_here
STREAMLIT_SECRET=optional_if_used
```

**Never upload your actual `.env` to GitHub!**

---

### 4. Running the Application

**Local:**

```bash
cd frontend_app
streamlit run app_ultimate.py
```

The backend and PDF logic will be auto-launched as part of Streamlit requests.

**Docker (for production or cloud):**

```bash
docker-compose up --build
```

---

## Usage

- Upload your source ("original") and submission documents in the interface.
- Select "Local Comparison" or "Internet Search" mode.
- View comparison with interactive, yellow-highlighted matches in real time.
- Download a detailed PDF plagiarism report—formatted for professional academic review.

---

## Security: Protecting Sensitive Data

- `.env` and all secrets are **excluded in `.gitignore`**.
- Only share `.env.example` and fill with dummy values.
- API keys should never be visible in the codebase, pdf reports, or public deployments!

---

## Customization & Extensions

- To add new plagiarism algorithms or APIs, update `backend_api/`.
- PDF and web UI themes can be adjusted in `professional_pdf_generator.py` and `app_ultimate.py`.
- You can swap Streamlit for any frontend with minimal backend changes.

---

## Credits

Developed by:  
- [Parag Khandare] (B.Tech Computer Science, Semester 7, RAIT)  


---

## For Demo or Production Deployment

- All secrets must be set with server-side environment variables or `.env`.
- For cloud: set up secrets in Deploy interface or CI/CD pipeline.
- All logs are non-sensitive and safe for classroom/college review.

---
