import configparser

config = configparser.ConfigParser()
config.read('config.ini')
default_section = config['DEFAULT']

source_KME_ID = default_section.get('source_KME_ID')
target_KME_ID = default_section.get('target_KME_ID')
master_SAE_ID = default_section.get('master_SAE_ID')
slave_SAE_ID = default_section.get('source_SAE_ID')
key_size = default_section.getint('key_size')
max_key_per_request = default_section.getint('max_key_per_request')
max_key_size = default_section.getint('max_key_size')
min_key_size = default_section.getint('min_key_size')
max_SAE_ID_count = default_section.getint('max_SAE_ID_count')
status_extension = default_section.get('status_extension')

print(source_KME_ID)