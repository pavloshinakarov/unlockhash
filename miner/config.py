import json
import uuid

def set_config_key(key, value):
    globals()[key] = value

with open("config.json") as json_config:
    config_data = json.load(json_config)

if not config_data.get("author"):
    config_data["author"] = str(uuid.uuid4())

    with open("config.json", "w") as json_out:
        json.dump(config_data, json_out, indent=2)

for key, value in config_data.items():
    set_config_key(key, value)

def update_config_key(key, value):
    with open("config.json") as json_config:
        config_data = json.load(json_config)

    config_data[key] = value

    with open("config.json", "w") as json_out:
        json.dump(config_data, json_out, indent=2)

    set_config_key(key, value)