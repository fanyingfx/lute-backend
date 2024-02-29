import tomllib
from pathlib import Path

path = Path("english.toml")

with path.open("rb") as f:
    data = tomllib.load(f)
# print(json.dumps(data, indent=4))
