# 🛠️ Data Pipeline Project

A modular and production-ready data pipeline built with **Python** that:

- 📤 Extracts data from **MySQL**
- ☁️ Stages it in **Amazon S3**
- 🧱 Loads it into **Amazon Redshift**

Supports both **full loads** and **incremental loads**, and is structured for clarity and maintainability.

---

## 📁 Project Structure

<pre lang="no-highlight"> ```text . ├── pipeline/ │ ├── extract_mysql_full.py │ └── extract_incremental.py │ ├── config/ │ ├── pipeline.conf # Git-ignored │ └── pipeline_template.conf # Safe public version │ ├── .gitignore ├── requirements.txt ├── README.md └── .venv/ ``` </pre>


