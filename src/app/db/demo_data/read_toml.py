import json
import tomllib

with open("english.toml", "rb") as f:
    data = tomllib.load(f)
print(json.dumps(data, indent=4))
