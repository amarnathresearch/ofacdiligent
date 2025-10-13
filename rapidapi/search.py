import http.client

conn = http.client.HTTPSConnection("yahoo-finance166.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "516121bb12mshf5a4ec7c789bd55p14db85jsn0a2d29113020",
    'x-rapidapi-host': "yahoo-finance166.p.rapidapi.com"
}

conn.request("GET", "/api/news/list-by-symbol?s=AAPL%2CGOOGL%2CTSLA&region=US&snippetCount=500", headers=headers)

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
with open("out1.json", "w", encoding="utf-8") as f:
    json.dump(parsed, f, indent=2, ensure_ascii=False)