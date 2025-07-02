# 🛠️ Data Pipeline Project

A modular and production-ready data pipeline built with **Python** that:

- 📤 Extracts data from **MySQL**
- ☁️ Stages it in **Amazon S3**
- 🧱 Loads it into **Amazon Redshift**

Supports both **full loads** and **incremental loads**, and is structured for clarity and maintainability.

---

## 📁 Project Structure

<pre lang="no-highlight"> 
  ├── pipeline/ # Core pipeline logic │ 
  ├── extract_mysql_full.py │ 
  └── extract_incremental.py │ 
  ├── config/ # Configuration files │
  ├── pipeline.conf # (Private – Git ignored) │ 
  ├── .gitignore 
  ├── requirements.txt 
  ├── README.md 
  └── .venv/ # Virtual environment (optional) 
  ``` </pre>
