import json
from types import SimpleNamespace

with open('config.json', 'r', encoding="utf-8") as config_file:
    data = config_file.read()

config = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

with open('test_config.json', 'r', encoding="utf-8") as config_file:
    data = config_file.read()

test_config = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

