import http.client

conn = http.client.HTTPSConnection("rauvaservicesunip.app.invoicexpress.com")

headers = { 'accept': "application/json" }

conn.request("GET", "/invoices.json?api_key=5a79167291dadd03d78781091f675786952c4e79&page=3", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
