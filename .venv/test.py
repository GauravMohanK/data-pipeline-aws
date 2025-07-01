import configparser

config_path = r"C:\Users\Gaura\data_pipeline_readwrite\pipeline.conf"
parser = configparser.ConfigParser()
parser.read(config_path)

print("Sections found:", parser.sections())
print("Hostname:", parser.get("mysql_config", "hostname"))
