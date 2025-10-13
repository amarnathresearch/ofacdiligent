import http.client
import json
import os

conn = http.client.HTTPSConnection("yahoo-finance-real-time1.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "516121bb12mshf5a4ec7c789bd55p14db85jsn0a2d29113020",
    'x-rapidapi-host': "yahoo-finance-real-time1.p.rapidapi.com"
}

conn.request("GET", "/stock/get-options?symbol=WOOF&lang=en-US&region=US", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
try:
    parsed = json.loads(data)
except json.JSONDecodeError:
    print("⚠️ Response was not valid JSON. Saving raw text instead.")
    parsed = {"raw_response": data}
# Save to file
with open("out.json", "w", encoding="utf-8") as f:
    json.dump(parsed, f, indent=2, ensure_ascii=False)

print("✅ Data saved to out.json")