import json
from jupyter_convert_core import parse_jupyter

with open("test.ipynb", "r", encoding="utf-8") as f:
    print(parse_jupyter(json.load(f)), sep="\n\n")
