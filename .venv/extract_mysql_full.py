import boto3
import configparser
import pymysql
import csv

# Read config file ONCE at the beginning
parser = configparser.ConfigParser()
parser.read(r"C:\Users\Gaura\data_pipeline_readwrite\pipeline.conf")

# Get MySQL configuration
hostname = parser.get("mysql_config", "hostname")
port = parser.get("mysql_config", "port")
username = parser.get("mysql_config", "username")
password = parser.get("mysql_config", "password")
dbname = parser.get("mysql_config", "database")

# Establish MySQL connection
conn = pymysql.connect(
    host=hostname,
    user=username,
    password=password,
    db=dbname,
    port=int(port)
)

if conn is None:
    print("Error connecting to the MySQL database")
else:
    print("MySQL connection established!")

# Extract data
m_query = "SELECT * FROM Orders;"
local_filename = "order_extract_full.csv"
m_cursor = conn.cursor()
m_cursor.execute(m_query)
results = m_cursor.fetchall()

# Write to CSV
with open(local_filename, 'w', newline='') as fp:  # Added newline=''
    csv_w = csv.writer(fp, delimiter='|')
    csv_w.writerows(results)

# Close resources
m_cursor.close()
conn.close()

# Get AWS credentials from SAME parser instance
access_key = parser.get("aws_boto_credentials", "access_key")
secret_key = parser.get("aws_boto_credentials", "secret_key")
bucket_name = parser.get("aws_boto_credentials", "bucket_name")

# Upload to S3
s3 = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)

s3.upload_file(local_filename, bucket_name, local_filename)  
