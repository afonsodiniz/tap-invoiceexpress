import http.client

conn = http.client.HTTPSConnection("rauvaportugalunip.app.invoicexpress.com")

headers = { 'accept': "application/json" }

conn.request("GET", "/invoices.json?api_key=API_KEY&page=3", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
