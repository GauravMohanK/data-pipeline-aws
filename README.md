# 🛠️ Data Pipeline Project

A Python-based data pipeline that:
- Extracts data from **MySQL**
- Stages it in **AWS S3**
- Loads it into **Amazon Redshift**

## 🚀 Features

- ✅ Full Load
- ✅ Incremental Load
- ✅ Modular and configurable

## 🔧 Tech Stack

- Python
- MySQL
- Amazon S3
- Amazon Redshift
- Boto3
- psycopg2 / SQLAlchemy

...

## 📁 Project Structure

<pre lang="no-highlight"> 
  ├── pipeline/ # Core pipeline logic │ 
  └── extract_mysql_full.py  
  └── extract_incremental.py 
  │ 
  ├── pipeline.conf # (Private – Git ignored) │ 
  ├── .gitignore 
  ├── requirements.txt  

   </pre>
