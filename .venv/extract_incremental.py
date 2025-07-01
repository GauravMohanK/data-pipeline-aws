import psycopg2
import configparser
import pymysql
import boto3
import csv

parser = configparser.ConfigParser()
parser.read(r"C:\Users\Gaura\data_pipeline_readwrite\pipeline.conf")

# Get connection parameters
dbname = parser.get("aws_creds", "database")
user = parser.get("aws_creds", "username")
password = parser.get("aws_creds", "password")
host = parser.get("aws_creds", "host")
port = parser.get("aws_creds", "port")

# Establish connection with SSL
rs_conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port,
    sslmode='require'  # Critical SSL parameter
)

rs_sql = """SELECT COALESCE(MAX(LastUpdated), '1900-01-01')
    FROM my_schema.Orders;"""
rs_cursor = rs_conn.cursor()
rs_cursor.execute(rs_sql)
result = rs_cursor.fetchone()

# there's only one row and column returned
last_updated_warehouse = result[0]

rs_cursor.close()
rs_conn.commit()

# get the MySQL connection info and connect
parser.read("pipeline.conf")
hostname = parser.get("mysql_config", "hostname")
port = parser.get("mysql_config", "port")
username = parser.get("mysql_config", "username")
dbname = parser.get("mysql_config", "database")
password = parser.get("mysql_config", "password")

conn = pymysql.connect(host=hostname,
        user=username,
        password=password,
        db=dbname,
        port=int(port), init_command="SET TIME_ZONE='+00:00'")



if conn is None:
  print("Error connecting to the MySQL database")
else:
  print("MySQL connection established!")

m_query = """SELECT *
    FROM Orders
    WHERE LastUpdated > %s;"""
local_filename = "order_extract.csv"

m_cursor = conn.cursor()
m_cursor.execute(m_query, (last_updated_warehouse,))
results = m_cursor.fetchall()

with open(local_filename, 'w') as fp:
  csv_w = csv.writer(fp, delimiter='|')
  csv_w.writerows(results)

fp.close()
m_cursor.close()
conn.close()

# load the aws_boto_credentials values
parser.read("pipeline.conf")
access_key = parser.get(
    "aws_boto_credentials",
    "access_key")
secret_key = parser.get(
    "aws_boto_credentials",
    "secret_key")
bucket_name = parser.get(
    "aws_boto_credentials",
    "bucket_name")

s3 = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key)

s3_file = local_filename

s3.upload_file(
    local_filename,
    bucket_name,
    s3_file)

copy_sql = f"""
COPY my_schema.orders
FROM 's3://{bucket_name}/{s3_file}'
IAM_ROLE 'arn:aws:iam::840473436290:role/RedShiftLoadRole'
DELIMITER '|'
IGNOREHEADER 0
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
BLANKSASNULL
EMPTYASNULL;
"""

rs_cursor = rs_conn.cursor()
rs_cursor.execute(copy_sql)
rs_conn.commit()
rs_cursor.close()
print("Data loaded into Redshift!")
print("last_updated_warehouse:", last_updated_warehouse, type(last_updated_warehouse))

