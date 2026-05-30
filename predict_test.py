import json
import urllib.request
from pathlib import Path

data = json.loads(Path("predict_input.json").read_text())
url = "http://localhost:8000/predict"
request = urllib.request.Request(
    url,
    data=json.dumps(data).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)
try:
    with urllib.request.urlopen(request) as response:
        print(response.status)
        print(response.read().decode())
except urllib.error.HTTPError as error:
    print("HTTPError", error.code)
    print(error.read().decode())
