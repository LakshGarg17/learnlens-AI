import urllib.request
import json

with open("sample_study_guide.pdf", "rb") as f:
    file_bytes = f.read()

boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
body = (
    f"--{boundary}\r\n"
    f'Content-Disposition: form-data; name="file"; filename="sample_study_guide.pdf"\r\n'
    f"Content-Type: application/pdf\r\n\r\n"
).encode("utf-8") + file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

req = urllib.request.Request(
    "http://127.0.0.1:8000/api/upload-pdf",
    data=body,
    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
)

try:
    resp = urllib.request.urlopen(req)
    print("HTTP Status:", resp.status)
    data = json.loads(resp.read().decode())
    print("Parsed JSON response:")
    print(json.dumps(data, indent=2))
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code, e.read().decode())
