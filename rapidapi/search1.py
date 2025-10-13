import http.client

conn = http.client.HTTPSConnection("yh-finance-pro-api.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "516121bb12mshf5a4ec7c789bd55p14db85jsn0a2d29113020",
    'x-rapidapi-host': "yh-finance-pro-api.p.rapidapi.com"
}

conn.request("GET", "/news?symbol=AAPL&count=10", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

import json
try:
    parsed = json.loads(data)
except json.JSONDecodeError:
    print("⚠️ Response was not valid JSON. Saving raw text instead.")
    parsed = {"raw_response": data}
# Save to file
with open("out2.json", "w", encoding="utf-8") as f:
    json.dump(parsed, f, indent=2, ensure_ascii=False)