import http.client

conn = http.client.HTTPSConnection("yahoo-finance-real-time1.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "516121bb12mshf5a4ec7c789bd55p14db85jsn0a2d29113020",
    'x-rapidapi-host': "yahoo-finance-real-time1.p.rapidapi.com"
}

conn.request("GET", "/stock/get-options?symbol=WOOF&lang=en-US&region=US", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))